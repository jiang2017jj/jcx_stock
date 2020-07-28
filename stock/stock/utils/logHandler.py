# -*- coding = utf-8 -*-
"""
@time:2020-07-02 15:10:59
@project:apiauto2020
@file:logHandler.py
@author:Jiang ChengLong
"""
import logging
import os
import sys
import time
import json
from logging import handlers
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from os import path

'''
filename    指定日志文件名
filemode    指定日志文件打开的模式，w 或 a
level       指定日志级别，默认 logging.WARNING
datefmt     使用指定的时间格式，format 参数中有 asctime 的话，需要使用 datefmt 指定格式
format      指定输出的格式和内容，format 的参考信息如下
format 输出格式参数
%(levelno)s:    打印日志级别的数值
%(levelname)s:  打印日志级别名称
%(pathname)s:   打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s:   打印当前执行程序名
%(funcName)s:   打印日志的当前函数
%(lineno)d:     打印日志的当前行号
%(asctime)s:    打印日志的时间
%(thread)d:     打印线程ID
%(threadName)s: 打印线程名称
%(process)d:    打印进程ID
%(message)s:    打印日志信息

# Python中的os模块用于和系统进行交互，其中：
# os.listdir()用于返回一个由文件名和目录名组成的列表，需要注意的是它接收的参数需要是一个绝对的路径。
# os.path.isdir()用于判断对象是否为一个目录。
# os.path.isfile()用于判断对象是否为一个文件。

# 获得某个路径的父级目录：
d = path.dirname(__file__)  # 返回当前文件所在的目录
# case_path = os.path.join(os.getcwd()) # 获取当前工作目录
# abspath = path.abspath(d) #返回d所在目录规范的绝对路径
parent_path = os.path.dirname(d)  # 获得d所在的目录,即d的父级目录
# parent_path  = os.path.dirname(parent_path) #获得parent_path所在的目录即parent_path的父级目录
# log_path是日志存放路径地址
'''

d = path.dirname(__file__)  # 返回当前文件所在的目录
parent_path = os.path.dirname(d)  # 获得d所在的目录,即d的父级目录
log_path = os.path.join(parent_path, 'logsfile')

# 日志类，支持输出到屏幕，支持输出到文件
class LogHandler():
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self):
        # log_path需要是个目录
        if os.path.isdir(log_path):
            # 日志文件的命名
            self.log_file_name = os.path.join(
                log_path, "%s.log" %
                time.strftime("%Y-%m-%d"))
            self.logger = logging.getLogger(self.log_file_name)
            self.logger.setLevel(self.level_relations.get('debug'))
            self.logFormat = '[%(asctime)s] - %(pathname)s[line: % (lineno)d] - [%(levelname)s]: [%(message)s]'
            # self.logFormat = '[%(asctime)s] -[%(filename)s] - [%(levelname)s]: [%(message)s]'
            self.dateFormat = '%Y-%m-%d %H:%M:%S'

    def save_debug_log_to_file_by_logging(self,str_word):
        # self.str_word = str_word
        try:
            logging.basicConfig(level=logging.DEBUG,  # 日志的严重程度,这个怎么确定的呢？
                                format=self.logFormat,  # 设置日志IDE输出格式
                                datefmt=self.dateFormat,  # 日期格式
                                filename=self.log_file_name,  # 日志保存到哪个文件
                                filemode='a')  # 日志记录的模式，a代表追加，w代表删除原有记录，重新创建新文件
            logging.info(str_word)

        except Exception as e:
            print(e)
            return None

    # 如果在logging.basicConfig()设置filename 和filemode，则只会保存log到文件，不会输出到控制台。
    # 由于在logging.basicConfig()中的level的值设置为logging.DEBUG, 所有debug, info, warning, error, critical 的log都会打印出来。
    # 直接使用logging输出日志到文件中
    def save_log_to_file_by_logging(
            self,
            casename,
            url,
            params,
            expect_res,
            when='D',
            backCount=3):
        try:
            logging.basicConfig(level=logging.DEBUG,  # 日志的严重程度,这个怎么确定的呢？
                                format=self.logFormat,  # 设置日志IDE输出格式
                                datefmt=self.dateFormat,  # 日期格式
                                filename=self.log_file_name,  # 日志保存到哪个文件
                                filemode='a')  # 日志记录的模式，a代表追加，w代表删除原有记录，重新创建新文件
            if isinstance(params, dict):
                params = json.dumps(
                    params, ensure_ascii=False)  # 如果data是字典格式，转化为字符串
            logging.info("测试用例：{}".format(casename))
            logging.info("请求url：{}".format(url))
            logging.info("请求参数：{}".format(params))
            logging.info("实际结果：{}".format(expect_res))
        except Exception as e:
            print(e)
            return None

    # 使用logger将日志输出到屏幕
    # 第一步，新建logger，设置 Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件，设置输出到file的log等级的开关
    # 第三步，再创建一个handler，用于输出到控制台，设置输出到console的log等级的开关
    # 第四步，定义handler的输出格式
    # 第五步，将logger添加到handler里面
    def save_log_to_screen(self, casename, url, params, expect_res):
        try:
            sh = logging.StreamHandler()  # 往屏幕上输出
            # 因为init文件中已经对logging.basicconfig进行了定义，下面两句可有可无；如果不定义logging.basicconfig，则需要有
            self.formatter = logging.Formatter(
                '[%(asctime)s] -[%(filename)s] - [%(levelname)s]: [%(message)s]')  # 设置日志格式
            sh.setFormatter(self.formatter)  # 设置屏幕上显示的格式
            self.logger.addHandler(sh)  # 把对象加到logger里
            if isinstance(params, dict):
                params = json.dumps(
                    params, ensure_ascii=False)  # 如果data是字典格式，转化为字符串
            self.logger.info("测试用例：{}".format(casename))
            self.logger.info("请求url：{}".format(url))
            self.logger.info("请求参数：{}".format(params))
            self.logger.info("实际结果：{}".format(expect_res))
        except Exception as e:
            print(e)
            return None

    # 使用logger将日志输出到文件中
    # 第一步，新建logger，设置 Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件，设置输出到file的log等级的开关
    # 第三步，再创建一个handler，用于输出到控制台，设置输出到console的log等级的开关
    # 第四步，定义handler的输出格式
    # 第五步，将logger添加到handler里面
    def save_log_to_file_by_logger(
            self,
            casename,
            url,
            params,
            expect_res,
            when='D',
            backCount=3):
        # 往文件里写入，如果需要比较复杂的功能，需要使用logger，如果简单存储日志使用logging即可
        # logger指定间隔时间自动生成文件的处理器，实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个数量，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        try:
            th = handlers.TimedRotatingFileHandler(
                filename=self.log_file_name,
                when=when,
                backupCount=backCount,
                encoding='utf-8')
            self.formatter = logging.Formatter(
                '[%(asctime)s] -[%(filename)s] - [%(levelname)s]: [%(message)s]')  # 设置日志格式
            th.setFormatter(self.formatter)  # 设置文件里写入的格式
            self.logger.addHandler(th)
            if isinstance(params, dict):
                params = json.dumps(
                    params, ensure_ascii=False)  # 如果data是字典格式，转化为字符串
            self.logger.info("测试用例：{}".format(casename))
            self.logger.info("请求url：{}".format(url))
            self.logger.info("请求参数：{}".format(params))
            self.logger.info("实际结果：{}".format(expect_res))
        except Exception as e:
            print(e)
            return None


'''
该日志类可以把不同级别的日志输出到不同的日志文件中，实现方法比较简单
'''
class Logger:
    def __init__(self):
        handlers = {
            logging.NOTSET: "logs/notset.log",
            logging.DEBUG: "logs/debug.log",
            logging.INFO: "logs/info.log",
            logging.WARNING: "logs/warning.log",
            logging.ERROR: "logs/error.log",
            logging.CRITICAL: "logs/critical.log",
        }
        self.__loggers = {}
        logLevels = handlers.keys()
        fmt = logging.Formatter('[%(asctime)s] - %(pathname)s[line: % (lineno)d] - [%(levelname)s]: [%(message)s]')
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



# 能够输出日志输出于哪个函数,比较朴素的实现，需要优化，让其更优雅
logLevels = [
    logging.NOTSET,
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]

class Jcl_Logger(object):
    def __init__(self, loggername):
        # 创建一个logger,不带参数则默认日志记录器名字为root，传入参数了日志记录器的名字就是传入的参数名
        self.logger = logging.getLogger(name=loggername)
        # 打印出debug级别以上的日志，debug info warnning error critial
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        # 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把logs变成文件名的一部分了
        # 这样写不好，windows系统用反斜杠\\ ,用join（）最佳
        # log_path = os.path.dirname(os.getcwd()) + "/logs/"
        # 指定输出的日志文件名
        # logname = log_path + 'out.log'

        # 创建日志文件名称。
        log_file_name = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))
        # 定义存储日志文件
        log_name = os.path.join(os.path.join(os.path.dirname(path.dirname(__file__)), 'logsfile'),(log_file_name + '.log'))

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_name,encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式，这个是关键了，拿到具体写入日志的函数名称,不生效！！！
        # 获取调用函数名
        funcName = sys._getframe().f_code.co_name
        # 获取行号
        lineNumber = sys._getframe().f_lineno

        # %(name)s是日志记录器的名字，这里应该是jcl_logger,
        # %(pathname)s调用日志记录函数的源码文件的全路径,
        # %(filename)spathname的文件名部分，包含文件后缀
        # %(funcName)s调用日志记录函数的函数名?是日志类定义所在的函数名
        formatter = logging.Formatter('%(asctime)s - %(process)d - %(threadName)s - %(thread)d - %(pathname)s - %(filename)s - %(module)s- %(funcName)s -%(lineno)d- %(levelname)s - %(message)s')
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    # 定义一个函数，回调logger实例
    def getlog(self):
        return self.logger


# 第二种，定义一个类，直接继承logging.Logger 那么就是说这个类就是一个Logger，有了Logger所有方法，在类里面添加一些内部方法，让logger封装addhandler, setformatter等方法
class LogHandler(logging.Logger):
    # 单例模式
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # 一开始居然用了 cls()来实例化 导致无限次调用
            # cls._instance = cls(*args, **kwargs)
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, name, level=logging.DEBUG, to_stream=True, to_file=True):
        self.name = name
        self.level = level
        self.formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        # 错误的， 继承了logger 本身就是logger 不用再self.logger=xxx 这样变成了一个新的变量
        #self.logger = logging.Logger(name=name, level=level)
        super(LogHandler, self).__init__(name=name, level=level)

        # 写文件
        if to_file:
            self.__setFileHandler__()

        # 写标准输出
        if to_stream:
            self.__setSteamHandler__()

    def __setSteamHandler__(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.addHandler(stream_handler)

    # 目录自己定义吧
    def __setFileHandler__(self):
        # 创建日志文件名称。
        log_file_name = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))
        # 定义存储日志文件
        log_name = os.path.join(os.path.join(os.getcwd(),'logs'),(log_file_name + '.log'))
        # 文件大小进行限制
        handler = RotatingFileHandler(log_name, maxBytes=1024, backupCount=5)
        handler.setFormatter(self.formatter)
        self.addHandler(handler)




# 第三种和第二种类似，亮点：TimedRotatingFileHandler支持日志回滚
# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

# 定义一个类，直接继承logging.Logger，亮点：支持日志回滚
class LogHandler(logging.Logger):
    """
    LogHandler
    """
    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def resetName(self, name):
        """
        reset name
        :param name:
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()




# 使用logging.basicConfig()实现，logging.basicConfig()函数是一个一次性的简单配置工具，
# 只有在第一次调用该函数时会起作用，后续再次调用该函数时完全不会产生任何操作的，多次调用的设置并不是累加操作。
def console_out(logFilename):
    ''''' Output log to file and console '''
    # Define a Handler and set a format which output to file
    logging.basicConfig(
        level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename=logFilename,  # log文件名
        filemode='w')  # 写入模式“w”或“a”
    # Define a Handler and set a format which output to console
    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.INFO)  # 定义该handler级别
    formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
    console.setFormatter(formatter)
    # Create an instance
    logging.getLogger().addHandler(console)  # 实例化添加handler

    # Print information              # 输出日志级别
    logging.debug('logger debug message')
    logging.info('logger info message')
    logging.warning('logger warning message')
    logging.error('logger error message')
    logging.critical('logger critical message')



# logging.config.dictConfig()：新建字典存储配置文件，然后将这个字典传给logging.config.dictConfig()
# 待补充
dictConfig = {
    'version': 1,
    'disable_existing_loggers': True,
    'incremental': False,
    'formatters': {
        'master_format': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(filename)s[line:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'filters': {
        'filter_by_name': {
            'class': 'logging.Filter',
            'name': 'fileLogger'
        },
        # 仅 INFO 能输出
        'filter_single_level_pass': {
            'class': 'logging.StreamHandler',
            'pass_level': logging.INFO
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'master_format',
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
            'level': logging.INFO,
            'formatter': 'master_format',
            'filters': ['filter_by_name', ],
        },
        'rotatingFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'rotatingLogfile.log',
            'level': logging.DEBUG,
            'formatter': 'master_format',
            'maxBytes': 256,
            'backupCount': 2
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console', ],
            'level': 'INFO',
            'propagate': False
        },
        'fileLogger': {
            'handlers': ['console', 'fileHandler'],
            'filters': ['filter_by_name', ],
            'level': 'DEBUG'
        },
        'rotatingFileLogger': {
            'handlers': ['console', 'rotatingFileHandler'],
            'level': 'INFO'
        }
    }
}
# logging.config.dictConfig(dictConfig)
# log = logging.getLogger(name='fileLogger')
# log.debug('log debug')
# log.info('log info')
# log.warning('log warning')
# log.error('log error')
# log.critical('log critical')
#
# log2 = logging.getLogger(name='rotatingFileLogger')
# log2.debug('log debug')
# log2.info('log info')
# log2.warning('log warning')
# log2.error('log error')
# log2.critical('log critical')





#logging.config.fileconfig()：创建一个日志配置文件，然后使用logging.config.fileconfig()函数来读取该文件的内容
#待补充
# logging.config.fileConfig('./logging.conf') # 路径不对，使用的时候继续完善
# log = logging.getLogger(name='rotatingFileLogger')
# log.debug('log debug')
# log.info('log info')
# log.warning('log warning')
# log.error('log error')
# log.critical('log critical')


if __name__ == "__main__":
    # log = LogHandler()
    # 将日志打到屏幕上,同时会默认也打印到文件里
    # log.save_log_to_screen('登录接口', 'www.baidu.com', 'a=1,b=2', 'jcl-0702')
    # 将日志保存到文件里,调用logger实现的方法，默认不会打印到屏幕上
    # log.save_log_to_file_by_logger(
    #   '登录接口', 'www.baidu.com', 'a=1,b=2', 'jcl-0702')
    # 将日志保存到文件里,调用logging实现的方法，默认不会打印到屏幕上
    # log.save_log_to_file_by_logging(
    #    '登录接口', 'www.baidu.com', 'a=1,b=2', 'jcl-0702')

    # 调试日志
    # log.save_debug_log_to_file_by_logging(u"调试信息")

    # logger = Logger()
    # logger.debug("thisisdebug")
    # logger.info("info")
    # logger.warning("warning")
    # logger.error("error")
    # logger.critical("critical")

    mylogger = Jcl_Logger('jcllogger')
    mylogger.getlog().debug('debug')
    mylogger.getlog().info('info')
    mylogger.getlog().warning('warnning')