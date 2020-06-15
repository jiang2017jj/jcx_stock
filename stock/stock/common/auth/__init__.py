# -*- coding = utf-8 -*-
"""
@time:2020-06-15 23:16:21
@project:stock
@file:__init__.py.py
@author:Jiang ChengLong
"""

from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

from app.auth import views
