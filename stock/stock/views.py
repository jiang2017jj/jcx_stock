# -*- coding = utf-8 -*-
"""
@time:2020-06-15 22:56:24
@project:stock
@file:views.py
@author:Jiang ChengLong
"""


from flask import Blueprint

user = Blueprint('user', __name__, url_prefix='/api')

from app.user import views
