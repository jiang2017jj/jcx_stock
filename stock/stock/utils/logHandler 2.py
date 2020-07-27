# -*- coding = utf-8 -*-
"""
@time:2020-07-10 11:00:37
@project:stock
@file:logHandler.py
@author:Jiang ChengLong
"""

import os
import sys
import logging

'''
如果更高端，则需要重新开发一个Python日志模块
Python自带的logging模块来打印日志，他功能强大，可以定制非常多的东西，
但当打印的日志的时候，根本不知道这条日志是在哪个地方打印的。里面的filename funcname都是日志类的信息，而不是调用者的信息
废了半天劲，擦泪！！！
'''

log_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")),'logs')
print(log_path)

class LogHandler:
    def __init__(self,log_path=log_path):
        handlers = {
            logging.NOTSET: os.path.join(log_path,'notset.log'),
            logging.DEBUG: os.path.join(log_path,'debug.log'),
            logging.INFO: os.path.join(log_path,'info.log'),
            logging.WARNING:os.path.join(log_path,'warning.log'),
            logging.ERROR: os.path.join(log_path,'error.log'),
            logging.CRITICAL: os.path.join(log_path,'critical.log')
        }
        self.__loggers = {}
        logLevels = handlers.keys()
        fmt = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        # fmt = logging.Formatter('%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s]: %(message)s')
        for level in logLevels:
            # 创建logger
            logger = logging.getLogger(str(level))
            logger.setLevel(level)
            # 创建hander用于写日日志文件
            log_path = os.path.abspath(handlers[level])
            fh = logging.FileHandler(log_path)
            # 定义日志的输出格式
            fh.setFormatter(fmt)
            fh.setLevel(level)
            # 给logger添加hander
            logger.addHandler(fh)
            self.__loggers.update({level: logger})

    def info(self, message):
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        self.__loggers[logging.ERROR].error(message)

    def warning(self, message):
        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        self.__loggers[logging.CRITICAL].critical(message)


if __name__ == "__main__":
    logger = LogHandler()
    logger.debug("debug级别的日志信息")
    logger.info("info级别的日志信息")
    logger.warning("warning级别的日志信息")
    logger.error("error级别的日志信息")
    logger.critical("critical级别的日志信息")