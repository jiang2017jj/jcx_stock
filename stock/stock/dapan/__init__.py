from flask import  Blueprint
#先导入蓝图函数
dapan_blue = Blueprint('dapan',__name__)

from  stock.dapan import views