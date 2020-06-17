# -*- coding = utf-8 -*-
"""
@time:2020-06-16 08:59:49
@project:stock
@file:time_handler.py
@author:Jiang ChengLong
"""

import os
import time
import json
import platform
import datetime

from config import VERSION


def get_timestamp(data=None, format="%Y-%m-%d %H:%M:%S"):
    """
    :param data:
    :param format:
    :return:
    """
    if data is None:
        data = time.time()
    return time.strftime(format, time.localtime(data))


def friendly_datetime(data):
    """
    # 将字典里的datetime类型转化为字符串格式，方便前端展示。
    :param data:
    :return:
    """
    if isinstance(data, (datetime.datetime,)):
        return data.strftime("%Y-%m-%d %H:%M:%S")

    if not isinstance(data, (dict,)):
        return data

    for key, value in data.items():
        if not isinstance(value, (datetime.datetime,)):
            continue
        data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    return data
