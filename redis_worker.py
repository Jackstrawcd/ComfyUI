#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4 10:57 AM
# @Author  : wangdongming
# @Site    : 
# @File    : redis_worker.py
# @Software: xingzhe.ai
import copy
import gc
import os.path
import random
import sys
import threading
import time
import logging
import traceback
import typing

import folder_paths
import nodes
import execution
import comfy.model_management
from worker.queue import RedisPromptQueue
from worker.fs import download_file, upload_image
from worker.task import TaskProgress, TaskStatus
from worker.test_task import TestTasks
from worker.environment import get_image_prefix_key, \
    get_ckpt_prefix_key, get_lora_prefix_key


def push_debug_task(server):
    q = RedisPromptQueue()
    for item in TestTasks:
        q.put(item)


def validate_prompt(prompt):
    outputs = set()
    for x in prompt:
        if 'class_type' not in prompt[x]:
            error = {
                "type": "invalid_prompt",
                "message": f"Cannot execute because a node is missing the class_type property.",
                "details": f"Node ID '#{x}'",
                "extra_info": {}
            }
            return (False, error, [], [])

        class_type = prompt[x]['class_type']
        class_ = nodes.NODE_CLASS_MAPPINGS.get(class_type, None)
        if class_ is None:
            error = {
                "type": "invalid_prompt",
                "message": f"Cannot execute because node {class_type} does not exist.",
                "details": f"Node ID '#{x}'",
                "extra_info": {}
            }
            return (False, error, [], [])

        if hasattr(class_, 'OUTPUT_NODE') and class_.OUTPUT_NODE is True:
            outputs.add(x)

    if len(outputs) == 0:
        error = {
            "type": "prompt_no_outputs",
            "message": "Prompt has no outputs",
            "details": "",
            "extra_info": {}
        }
        return (False, error, [], [])

    return (True, None, list(outputs), [])


def get_dir_by_type(dir_type):
    if dir_type is None:
        dir_type = "input"

    if dir_type == "input":
        type_dir = folder_paths.get_input_directory()
    elif dir_type == "temp":
        type_dir = folder_paths.get_temp_directory()
    elif dir_type == "output":
        type_dir = folder_paths.get_output_directory()

    return type_dir, dir_type


def prepare_worker(prompt: typing.Mapping):
    for i, node in prompt.items():
        class_type = node['class_type']
        inputs = node['inputs']
        if class_type == 'CheckpointLoaderSimple':
            ckpt_name = os.path.basename(inputs['ckpt_name'])
            local = os.path.join('models', 'checkpoints', ckpt_name)

            dirname = os.path.dirname(inputs['ckpt_name'])
            if not dirname:
                dirname = get_ckpt_prefix_key()

            ok = download_file(os.path.join(dirname, ckpt_name), local)
            if ok:
                prompt[i]['inputs']['ckpt_name'] = ckpt_name
        elif class_type == 'LoraLoader':
            lora_name = os.path.basename(inputs['lora_name'])
            local = os.path.join('models', 'loras', lora_name)

            dirname = os.path.dirname(inputs['lora_name'])
            if not dirname:
                dirname = get_lora_prefix_key()

            ok = download_file(os.path.join(dirname, lora_name), local)
            if ok:
                prompt[i]['inputs']['lora_name'] = lora_name
        elif class_type == 'LoadImage':
            filename, output_dir = folder_paths.annotated_filepath(inputs.get('filename') or inputs.get('image'))
            image_name = os.path.basename(filename)
            local_dir, _ = get_dir_by_type('input')
            local = os.path.join(output_dir or local_dir, image_name)

            dirname = os.path.dirname(filename)
            if not dirname:
                dirname = get_image_prefix_key()
            else:
                dirname = os.path.join(get_image_prefix_key(), dirname)

            ok = download_file(os.path.join(dirname, image_name), local)
            if ok:
                prompt[i]['inputs']['image'] = image_name
        elif class_type == 'LoadImageMask':
            pass


def upload_outputs(outputs_ui: dict):
    for k, v in outputs_ui.items():
        images = v.get('images') or []
        for i, image_item in enumerate(images):
            filename = image_item['filename']
            subfolder = image_item['subfolder']
            file_type = image_item['type']
            local_dir, _ = get_dir_by_type(file_type)
            if subfolder:
                local_dir = os.path.join(local_dir, subfolder)
            local = os.path.join(local_dir, filename)
            remoting = upload_image(local)
            if not remoting:
                raise OSError(f'cannot upload image:{local}')
            outputs_ui[k]['images'][i]['filename'] = remoting


def prompt_worker(server):
    e = execution.PromptExecutor(server)
    last_gc_collect = 0
    need_gc = False
    gc_collect_interval = 10.0
    q = RedisPromptQueue()
    current_time = 0

    def exec_task(task_progress: TaskProgress):
        task_progress.prepare()
        yield task_progress

        prompt = task_progress.task.get('prompt')
        extra_data = task_progress.task.get('extra_data', {})
        outputs_to_execute = task_progress.task.get('outputs_to_execute', {})

        prepare_worker(prompt)

        task_progress.progress(0)
        yield task_progress

        prompt_id = task_progress.task.task_id
        e.execute(prompt, prompt_id, extra_data, outputs_to_execute)
        if e.success:
            task_progress.progress(90, status=TaskStatus.Uploading)
            yield task_progress

            outputs = copy.deepcopy(e.outputs_ui)
            upload_outputs(outputs)
            task_progress.ok(outputs)
        else:
            task_progress.failed(msg=e.status_messages)
        yield task_progress

    while True:
        timeout = 1000.0
        if need_gc:
            timeout = max(gc_collect_interval - (current_time - last_gc_collect), 0.0)

        task_progress = q.get(validate_prompt, server.trigger_on_prompt, timeout=timeout)
        if task_progress is not None:
            execution_start_time = time.perf_counter()
            prompt_id = task_progress.task.task_id
            server.last_prompt_id = prompt_id
            logging.info(f"execute task {prompt_id}")
            try:
                for p in exec_task(task_progress):
                    q.progress_changed(p)
            except Exception as err:
                trace = traceback.format_exc()
                task_progress.failed(trace, str(err))
                logging.exception("exec task failed")
                try:
                    q.progress_changed(task_progress)
                except Exception:
                    logging.exception('cannot dump task progress')

            current_time = time.perf_counter()
            execution_time = current_time - execution_start_time
            logging.info("Prompt executed in {:.2f} seconds".format(execution_time))

        free_memory = random.randint(0, 10) < 5
        unload_models = random.randint(0, 10) < 5

        if unload_models:
            comfy.model_management.unload_all_models()
            need_gc = True
            last_gc_collect = 0

        if free_memory:
            e.reset()
            need_gc = True
            last_gc_collect = 0

        if need_gc:
            current_time = time.perf_counter()
            if (current_time - last_gc_collect) > gc_collect_interval:
                comfy.model_management.cleanup_models()
                gc.collect()
                comfy.model_management.soft_empty_cache()
                last_gc_collect = current_time
                need_gc = False


def run_redis_prompt_worker(server, debug_task=True):
    if debug_task:
        push_debug_task(server)

    threading.Thread(target=prompt_worker, daemon=True, args=(server,)).start()
