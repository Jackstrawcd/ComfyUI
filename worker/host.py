#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4 5:38 PM
# @Author  : wangdongming
# @Site    : 
# @File    : host.py
# @Software: xingzhe.ai
import socket
import time


def get_host_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s:
            s.close()
    return ip


def get_host_name(retry_times=0, delay=2):
    retry_times = retry_times if retry_times > 0 else 1
    for _ in range(retry_times):
        try:
            hostname = socket.gethostname()
            return hostname
        except Exception as err:
            logger.warning(f"cannot get host name:{err}")
            time.sleep(delay)
    return None

