# 导入的Flask类，这个类的实例化的对象就是我们的WSGI应用程序
import logging
from logging.config import fileConfig

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import atexit
import platform

import logconfig
from config import config
from stock.tasks.task_init import quality_apscheduler

blueprints = [
    # 'clover.suite:suite',
    # 'clover.interface:interface',
    # 'clover.environment:environment',
]

mail = Mail()
moment = Moment()
db = SQLAlchemy(use_native_unicode='utf8')

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = u"请登录stock平台"


def create_app(config_name):
    # app就是一个WSGI应用程序，单一模块第一个参数为__name__，此处需要后续考察下是否正确
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.app_context().push()
    # 支持json显示中文
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config[config_name]) # 把全局config中的配置读取
    config[config_name].init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # 注册和初始化apscheduler,否则无法执行定时任务，在tasks.task_init.py下quality_apscheduler = BackgroundScheduler()
    # 1.定时器调度(app初始化过程中会执行),必须确保使用aspcheduler对象的时候已经安装到app上
    # 2.api调用，app初始化完毕后才会执行，顺序要对
    # if os.environ.get("WERKZEUG_RUN_MAIN")==True:
    # quality_apscheduler.init_app(app)  # 把任务列表放进flask
    # quality_apscheduler.start() # 启动任务列表
    scheduler_init(app)

    return app


# 如果在create_app（）里直接初始化了quality_apscheduler，此时如果debug=True，则定时任务重复执行，
# 解决方法有2种，都可以：
# 1.debug改为false,已经验证，可行；
# 2.使用文件锁,网上找到锁的代码，可行；
def scheduler_init(app):
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            quality_apscheduler.init_app(app)
            quality_apscheduler.start()
            # app.logger.debug('Scheduler Started,---------------')
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            quality_apscheduler.init_app(app)
            quality_apscheduler.start()
            # app.logger.debug('Scheduler Started,----------------')
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)



# 加载日志文件的时候应该尽可能的早，避免在调用过一次app.logger之后才加载日志配置，所以最好在app被创建之前就加载日志配置文件。
logging.config.fileConfig(logconfig.logger_dict)


# 本地开发使用
# app = create_app('development')

# 提交代码到qa时使用
app = create_app('testing')

# 提交代码到生产时使用
# app = create_app('production')