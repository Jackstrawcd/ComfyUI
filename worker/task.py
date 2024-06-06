#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3 6:20 PM
# @Author  : wangdongming
# @Site    : 
# @File    : task.py
# @Software: xingzhe.ai
import enum
import time
import typing
from collections import UserDict


class SerializationObj:

    def to_dict(self):
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            try:
                if not name.startswith('_') and not callable(value):
                    if hasattr(value, 'to_dict'):
                        to_dict_func = getattr(value, 'to_dict')
                        if callable(to_dict_func):
                            value = value.to_dict()
                    pr[name] = value
            except:
                pass
        return pr


class Task(UserDict):

    def __init__(self, **meta):
        task_id = meta.get('task_id')
        if not task_id:
            raise KeyError('cannot found task id')
        task_type = meta.get('task_type')
        if not task_type:
            raise KeyError('cannot found task type')
        super(Task, self).__init__(None, **meta)
        self.task_type = task_type
        self.task_id = task_id
        self.setdefault('create_at', int(time.time()))


class TaskStatus(enum.IntEnum):
    Failed = -1
    Waiting = 0
    Prepare = 1
    Ready = 2
    Running = 3
    Uploading = 4
    OK = 10


class TaskProgress(UserDict):

    def __init__(self, task: Task):
        self.task = task
        d = {
            'task': dict(task),
            'result': None,
            'msg': '',
            'progress': 0,
            'traceback': '',
            'status': TaskStatus.Waiting
        }
        super(TaskProgress, self).__init__(d)

    def ok(self, r: typing.Mapping):
        self['msg'] = 'ok'
        self['progress'] = 100
        self['result'] = r
        self['status'] = TaskStatus.OK

    def failed(self, trace: str = None, msg: str = None):
        self['msg'] = msg or 'failed'
        self['traceback'] = trace
        self['status'] = TaskStatus.Failed

    def progress(self, p: float, msg: str = None, status: TaskStatus = TaskStatus.Running):
        if self['progress'] > p:
            return
        self['msg'] = msg or 'running'
        self['progress'] = p
        self['status'] = status

    def prepare(self):
        self['msg'] = 'prepare'
        self['progress'] = 0
        self['status'] = TaskStatus.Prepare

    def ready(self):
        self['msg'] = 'ready'
        self['progress'] = 0
        self['status'] = TaskStatus.Ready
