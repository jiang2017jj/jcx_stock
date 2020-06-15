# -*- coding = utf-8 -*-
"""
@time:2020-06-15 23:27:36
@project:stock
@file:__init__.py.py
@author:Jiang ChengLong
"""
from flask import  Blueprint
#先导入蓝图函数
dapan_blue = Blueprint('dapan',__name__)

from  stock.dapan import views