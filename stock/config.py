DEBUG = True
VERSION = '0.0.1'

MYSQL = {
    'user': 'stock',
    'pswd': '123456',
    'host': '127.0.0.1',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/stock?charset=utf8'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS=True

CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND=''
#http://www.avsc5.com/list/14-10.html
