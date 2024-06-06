#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3 4:52 PM
# @Author  : wangdongming
# @Site    : 
# @File    : queue.py
# @Software: xingzhe.ai
import json
import logging
import threading
import time
import typing
import uuid
from .task import Task, TaskProgress
from .redis import RedisPool
from .environment import get_comfy_task_queue_name


class RedisPromptQueue:

    def __init__(self):
        self.mutex = threading.RLock()
        self.redis_pool = RedisPool()
        self.queue_name = get_comfy_task_queue_name()

    def item2task(self, item: dict,
                  validate_prompt: typing.Callable=None,
                  trigger_on_prompt: typing.Callable=None) -> typing.Optional[Task]:
        json_data = trigger_on_prompt(item)
        if "prompt" in item:
            prompt = json_data["prompt"]
            valid = validate_prompt(prompt)
            extra_data = {}
            if "extra_data" in json_data:
                extra_data = json_data["extra_data"]

            if "client_id" in json_data:
                extra_data["client_id"] = json_data["client_id"]
            if valid[0]:
                prompt_id = str(uuid.uuid4())
                outputs_to_execute = valid[2]
                # number, prompt_id, prompt, extra_data, outputs_to_execute
                d = {
                    'task_id': prompt_id,
                    'extra_data': extra_data,
                    'outputs_to_execute': outputs_to_execute,
                    'prompt': prompt,
                    'task_type': 1,
                }

                t = Task(**d)
                return t

    def put(self, item):
        '''
        put task to queue.

        '''
        # t = self.item2task(item, validate_prompt, trigger_on_prompt)
        # if not t:
        #     raise ValueError('cannot convert task')
        rds = self.redis_pool.get_connection()
        rds.rpush(self.queue_name, json.dumps(dict(item)))

    def get(self, validate_prompt, trigger_on_prompt, timeout=None) -> typing.Optional[TaskProgress]:
        timeout = timeout or 1
        for i in range(int(timeout)):
            try:
                rds = self.redis_pool.get_connection()
                task = rds.lpop(self.queue_name)
            except:
                task = None
            if task:
                json_data = json.loads(task)
                task_id = json_data['task_id']

                t = self.item2task(json_data, validate_prompt, trigger_on_prompt)
                if not t:
                    raise ValueError(f'cannot validate task info: {task_id}')
                p = TaskProgress(t)
                return p
            else:
                time.sleep(1)
                if i % 60 == 0:
                    logging.info("waiting task...")

    def task_done(self, p: TaskProgress):
        self.progress_changed(p)

    def progress_changed(self, p: TaskProgress):
        with self.mutex:
            rds = self.redis_pool.get_connection()
            task_id = p.task.task_id
            rds.setex(task_id, 3600 * 4, json.dumps(dict(p)))


