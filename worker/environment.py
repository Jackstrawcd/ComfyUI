#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3 4:57 PM
# @Author  : wangdongming
# @Site    : 
# @File    : environment.py
# @Software: xingzhe.ai

import os
import typing


Env_RedisHost = 'RedisHost'
Env_RedisPass = 'RedisPass'
Env_RedisPort = 'RedisPort'
Env_RedisUser = 'RedisUser'
Env_RedisDB = 'RedisDB'
Env_MgoHost = 'MgoHost'
Env_MgoUser = 'MgoUser'
Env_MgoPass = 'MgoPass'
Env_MgoPort = 'MgoPort'
Env_MgoDB = 'MgoDB'
Env_MgoDocExp = "MgoDocExpSec"
Env_MgoCollect = 'MgoCollect'
Env_EndponitKey = 'StorageEndponit'
Env_AccessKey = 'StorageAK'
Env_SecretKey = 'StorageSK'
Env_BucketKey = 'StorageBucket'
Env_QueueName = "ComfyTaskQueueName"
Env_ImagePrefixKey = 'ImagePrefixKey'
Env_LoraPrefixKey = 'LoraPrefixKey'
Env_CkptPrefixKey = 'CkptPrefixKey'

DefImagePrefixKey = "comfyui/images/"
DefLoraPrefixKey = "comfyui/loras/"
DefCkptPrefixKey = "comfyui/checkpoint/"
DefComfyTaskQueue = 'comfyui_task'
cache = {}


def get_value_from_env(k, defalut=None):
    if k not in cache:
        cache[k] = os.getenv(k) or defalut
    return cache[k]


def mongo_doc_expire_seconds():
    '''
    获取MONGO文档过期时间，0代表不过期
    '''
    try:
        exp = os.getenv(Env_MgoDocExp, 0)
        exp = int(exp)
    except:
        exp = 0
    return exp


def get_comfy_task_queue_name():
    return get_value_from_env(Env_QueueName, DefComfyTaskQueue)


def get_image_prefix_key():
    return get_value_from_env(Env_ImagePrefixKey, DefImagePrefixKey)


def get_lora_prefix_key():
    return get_value_from_env(Env_LoraPrefixKey, DefLoraPrefixKey)


def get_ckpt_prefix_key():
    return get_value_from_env(Env_CkptPrefixKey, DefCkptPrefixKey)


def get_file_storage_system_env() -> typing.Mapping[str, str]:
    d = {
        Env_EndponitKey: None,
        Env_AccessKey: None,
        Env_SecretKey: None,
        Env_BucketKey: None,
    }
    for key in d.keys():
        d[key] = cache.get(key) or os.getenv(key)
        cache[key] = d[key]
    return d


def get_redis_env() -> typing.Mapping[str, str]:
    d = {
        Env_RedisPort: None,
        Env_RedisDB: None,
        Env_RedisPass: None,
        Env_RedisHost: None,
        Env_RedisUser: None
    }
    for key in d.keys():
        d[key] = cache.get(key) or os.getenv(key)
        cache[key] = d[key]
    return d


def get_mongo_env() -> typing.Mapping[str, str]:
    d = {
        Env_MgoHost: None,
        Env_MgoUser: None,
        Env_MgoPass: None,
        Env_MgoPort: None,
        Env_MgoDB: None,
        Env_MgoCollect: None,
    }
    for key in d.keys():
        d[key] = cache.get(key) or os.getenv(key)
        cache[key] = d[key]
    return d


