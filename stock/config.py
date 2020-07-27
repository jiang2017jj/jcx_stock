import os

# stock 版本配置，最终production分支的版本为准
VERSION = '0.0.1'

# BASEDIR此时是值的工程文件夹目录/stock
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# 定义配置类基类
class Config:

    # 如何生成强壮的密钥，首先import os,然后os.urandom(24)即可
    SECRET_KEY = 'jcl_secret_key'

    # SQLALCHEMY修改的跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY拆卸时提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 在用配置类的方式给app设置配置时, SQLALCHEMY_ECHO 这个是记录打印SQL语句用于调试的, 一般设置为False, 不然会在控制台输出一大堆的东西
    SQLALCHEMY_ECHO = True
    # 邮件标题前缀
    FLASKY_MAIL_SUBJECT_PREFIX = 'Stock is wealth'

    # ldap配置
    LDAP_HOST = "ldaps://ad01.xiaobang.xyz"
    LDAP_ADMIN = {
        "user": "wechat_sync@xiaobang.xyz",
        "pwd": "JWPRj7pa^J#3NLZ3"
    }

    # 微信配置
    WECHAT_CONFIG = {
        "corp_id": "wwf1143b4d1547c208",
        "corp_secret": "IyrzR40w1pK2nVWEYIxWCQ9LkOWw7Wrcf45PTEubbV4"
    }

    # git sever地址配置
    GIT_SERVER="http://code.xiaobangtouzi.com/"

    # jira server地址配置
    JIRA_SERVER="http://jira.xiaobangtouzi.com/"

    #新增一个APScheduler的API的开关
    SCHEDULER_API_ENABLED = True

    # 便于调试
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0


    # 静态方法，可以直接类名调用，修饰的函数参数不需要第一个是self参数，用于执行环境的初始化
    @staticmethod
    def init_app(app):
        return u'环境初始化成功'


# 开发环境
class DevelopmentConfig(Config):
    # 全局配置
    DEBUG = True
    # mysql配置
    MYSQL = {
        'dialect':'mysql',
        'driver':'pymysql',
        'user': 'stock',
        'pswd': '123456',
        'host': '127.0.0.1',
        'port': '3306',
        'database':'stock',
    }
    SQLALCHEMY_DATABASE_URI = '{dialect}+{driver}://{user}:{pswd}@{host}:{port}/{database}?charset=utf8'.format(**MYSQL)
    SQLALCHEMY_POOL_RECYCLE = 3599
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")

    # redis配置，使用redis作为消息队列，如果必要还要进行设置缓存；废除celery
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DATABASE = 0
    # celery有问题，不再用来作为消息队列使用，废弃
    # CELERY_RESULT_BACKEND=''
    # http://www.avsc5.com/list/14-10.html

    # 功能控制,作为一个开关，用来判断是否展示在前端页面上，True则生效，False则无效
    MODULE = {
        'join_us': True,  # 展示加入我们
        'task': False  # 开发中的定时任务
    }

    # 企业微信配置
    WECHAT = {
        'key': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',  # 这里是企业微信机器人的key
        'template': {
            'msgtype': 'markdown',
            'markdown': {
                'content': 'Clover平台运行报告！\n' +
                           '>类型:<font color=\"comment\">{type}</font>\n' +
                           '>团队:<font color=\"comment\">{team}</font>\n' +
                           '>项目:<font color=\"comment\">{project}</font>\n' +
                           '>名称:<font color=\"comment\">{name}</font>\n' +
                           '>接口:<font color=\"comment\">{interface}个</font>\n' +
                           '>断言:<font color=\"comment\">{verify}个</font>\n' +
                           '>成功率:<font color=\"comment\">{percent}</font>\n' +
                           '>开始时间:<font color=\"comment\">{start}</font>\n' +
                           '>结束时间:<font color=\"comment\">{end}</font>\n' +
                           '[测试报告-{id}](http://www.52clover.cn/report/detail?id={id})'
            }
        }
    }

    # 邮箱配置
    # FLASKY_MAIL_SENDER = 'jcl'
    # FLASKY_ADMIN = 'jcl_admin'
    # MAIL_SERVER = 'smtp.exmail.qq.com'
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = 'jiangchenglong@xiaobangtouzi.com'
    # MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    EMAIL = {
        'sender': '12345678@qq.com',
        'receiver': ['12345678@qq.com'],
        'password': '',
        'smtp_host': 'smtp.qq.com',
    }

    NOTIFY = {
        # 通知的触发事件，成功时通知还是失败时通知
        'event': ['success', 'failed'],
        # 通知的方式，企业微信还是email，或则配置的其它方式
        'channel': ['email'],
    }


    # 注意：需要定时执行的job只需要在这添加配置！
    JOBS = [
      {
          'id': 'jcl_0109_job001',
          'func': job_1,
          'args': None,
          'trigger': {
              'type': 'cron', # 类型
              'day_of_week': "0-6",	# 可定义具体哪几天要执行
              'hour': '22',	# 小时数
              'minute': '0'
          }
      }
      # {
      #   'id': 'jcl_0109_job002',
      #   'func': job_1,
      #   'args': '',
      #   'trigger': 'interval',
      #   'seconds': 5  # 每隔5秒执行一次
      # },
      # {
      # 	'id': 'jcl_0109_job003',
      # 	'func': 'job_1',
      #   # 一次性任务可以省略trigger
      # 	'args': None,
      # 	'next_run_time': datetime.datetime.now() + datetime.timedelta(seconds=10)
      # }
    ]


# 测试环境
class TestingConfig(Config):
    # 全局配置
    DEBUG = True
    # mysql配置
    MYSQL = {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'user': 'stock',
        'pswd': '123456',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'stock',
    }
    SQLALCHEMY_DATABASE_URI = '{dialect}+{driver}://{user}:{pswd}@{host}:{port}/{database}?charset=utf8'.format(**MYSQL)
    SQLALCHEMY_POOL_RECYCLE = 3599
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")

    # redis配置，使用redis作为消息队列，如果必要还要进行设置缓存；废除celery
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DATABASE = 0
    # celery有问题，不再用来作为消息队列使用，废弃
    # CELERY_RESULT_BACKEND=''
    # http://www.avsc5.com/list/14-10.html

    # 功能控制,作为一个开关，用来判断是否展示在前端页面上，True则生效，False则无效
    MODULE = {
        'join_us': True,  # 展示加入我们
        'task': False  # 开发中的定时任务
    }

    # 企业微信配置
    WECHAT = {
        'key': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',  # 这里是企业微信机器人的key
        'template': {
            'msgtype': 'markdown',
            'markdown': {
                'content': 'Clover平台运行报告！\n' +
                           '>类型:<font color=\"comment\">{type}</font>\n' +
                           '>团队:<font color=\"comment\">{team}</font>\n' +
                           '>项目:<font color=\"comment\">{project}</font>\n' +
                           '>名称:<font color=\"comment\">{name}</font>\n' +
                           '>接口:<font color=\"comment\">{interface}个</font>\n' +
                           '>断言:<font color=\"comment\">{verify}个</font>\n' +
                           '>成功率:<font color=\"comment\">{percent}</font>\n' +
                           '>开始时间:<font color=\"comment\">{start}</font>\n' +
                           '>结束时间:<font color=\"comment\">{end}</font>\n' +
                           '[测试报告-{id}](http://www.52clover.cn/report/detail?id={id})'
            }
        }
    }

    # 邮箱配置
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    FLASKY_MAIL_SENDER = 'jcl'
    FLASKY_ADMIN = 'jcl_admin'
    MAIL_USERNAME = 'jiangchenglong@xiaobangtouzi.com'
    MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    # EMAIL = {
    #     'sender': '12345678@qq.com',
    #     'receiver': ['12345678@qq.com'],
    #     'password': '',
    #     'smtp_host': 'smtp.qq.com',
    # }

    NOTIFY = {
        # 通知的触发事件，成功时通知还是失败时通知
        'event': ['success', 'failed'],
        # 通知的方式，企业微信还是email，或则配置的其它方式
        'channel': ['email'],
    }

    # 注意：需要定时执行的job只需要在这添加配置！
    JOBS = [
        {
            'id': 'jcl_0109_job001',
            'func': job_1,
            'args': None,
            'trigger': {
                'type': 'cron',  # 类型
                'day_of_week': "0-6",  # 可定义具体哪几天要执行
                'hour': '22',  # 小时数
                'minute': '0'
            }
        }
        # {
        #   'id': 'jcl_0109_job002',
        #   'func': job_1,
        #   'args': '',
        #   'trigger': 'interval',
        #   'seconds': 5  # 每隔5秒执行一次
        # },
        # {
        # 	'id': 'jcl_0109_job003',
        # 	'func': 'job_1',
        #   # 一次性任务可以省略trigger
        # 	'args': None,
        # 	'next_run_time': datetime.datetime.now() + datetime.timedelta(seconds=10)
        # }
    ]

# 生产环境
class ProductionConfig(Config):
    # 全局配置
    DEBUG = True
    # mysql配置
    MYSQL = {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'user': 'stock',
        'pswd': '123456',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'stock',
    }
    SQLALCHEMY_DATABASE_URI = '{dialect}+{driver}://{user}:{pswd}@{host}:{port}/{database}?charset=utf8'.format(**MYSQL)
    SQLALCHEMY_POOL_RECYCLE = 3599
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")

    # redis配置，使用redis作为消息队列，如果必要还要进行设置缓存；废除celery
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DATABASE = 0
    # celery有问题，不再用来作为消息队列使用，废弃
    # CELERY_RESULT_BACKEND=''
    # http://www.avsc5.com/list/14-10.html

    # 功能控制,作为一个开关，用来判断是否展示在前端页面上，True则生效，False则无效
    MODULE = {
        'join_us': True,  # 展示加入我们
        'task': False  # 开发中的定时任务
    }

    # 企业微信配置
    WECHAT = {
        'key': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',  # 这里是企业微信机器人的key
        'template': {
            'msgtype': 'markdown',
            'markdown': {
                'content': 'Clover平台运行报告！\n' +
                           '>类型:<font color=\"comment\">{type}</font>\n' +
                           '>团队:<font color=\"comment\">{team}</font>\n' +
                           '>项目:<font color=\"comment\">{project}</font>\n' +
                           '>名称:<font color=\"comment\">{name}</font>\n' +
                           '>接口:<font color=\"comment\">{interface}个</font>\n' +
                           '>断言:<font color=\"comment\">{verify}个</font>\n' +
                           '>成功率:<font color=\"comment\">{percent}</font>\n' +
                           '>开始时间:<font color=\"comment\">{start}</font>\n' +
                           '>结束时间:<font color=\"comment\">{end}</font>\n' +
                           '[测试报告-{id}](http://www.52clover.cn/report/detail?id={id})'
            }
        }
    }

    # 邮箱配置
    FLASKY_MAIL_SENDER = 'jcl'
    FLASKY_ADMIN = 'jcl_admin'
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'jiangchenglong@xiaobangtouzi.com'
    MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    # EMAIL = {
    #     'sender': '12345678@qq.com',
    #     'receiver': ['12345678@qq.com'],
    #     'password': '',
    #     'smtp_host': 'smtp.qq.com',
    # }

    NOTIFY = {
        # 通知的触发事件，成功时通知还是失败时通知
        'event': ['success', 'failed'],
        # 通知的方式，企业微信还是email，或则配置的其它方式
        'channel': ['email'],
    }

    # 注意：需要定时执行的job只需要在这添加配置！
    JOBS = [
        {
            'id': 'jcl_0109_job001',
            'func': job_1,
            'args': None,
            'trigger': {
                'type': 'cron',  # 类型
                'day_of_week': "0-6",  # 可定义具体哪几天要执行
                'hour': '22',  # 小时数
                'minute': '0'
            }
        }
        # {
        #   'id': 'jcl_0109_job002',
        #   'func': job_1,
        #   'args': '',
        #   'trigger': 'interval',
        #   'seconds': 5  # 每隔5秒执行一次
        # },
        # {
        # 	'id': 'jcl_0109_job003',
        # 	'func': 'job_1',
        #   # 一次性任务可以省略trigger
        # 	'args': None,
        # 	'next_run_time': datetime.datetime.now() + datetime.timedelta(seconds=10)
        # }
    ]




config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': TestingConfig
}
