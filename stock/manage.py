
import pymysql
from flask_script import Server
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from werkzeug.utils import import_string
from stock import app, db
# orm的模型类需要导入
# from app.submit.models import SubmitData,TestReportData,CostTimeData

pymysql.install_as_MySQLdb()

CORS(app, supports_credentials=True)

# 这里后续可以放到配置文件中，每次增加一个模块增加一个配置即可。
blueprints = [
    'stock.dapan:dapan_blue'
]

# 新增子app，需要注册蓝图
for bp_name in blueprints:
    bp = import_string(bp_name)
    app.register_blueprint(bp)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=make_shell_context))

# 在调试模式下，Flask的重新加载器将加载烧瓶应用程序两次。
# 因此flask总共有两个进程. 重新加载器监视文件系统的更改并在不同的进程中启动真实应用程序
if __name__ == '__main__':
    manager.run()


