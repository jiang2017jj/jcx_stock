#!/usr/bin/env python3
#-*- coding = utf-8 -*-

"""
@time:2020-07-27 19:06:26
@project:stock
@file:logconfig.py
@author:Jiang ChengLong
"""
# 日志
logger_dict = {
    'version': 1, # 该配置写法固定
    'formatters': { # 设置输出格式
        'default': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',}
    },
    # 设置处理器
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'level': 'DEBUG'
                }},
    # 设置root日志对象配置
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    # 设置其他日志对象配置
    'loggers': {
        'test':
            {'level': 'DEBUG',
             'handlers':['wsgi'],
             'propagate':0}
    }
}