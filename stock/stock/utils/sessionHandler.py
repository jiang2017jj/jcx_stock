# -*- coding = utf-8 -*-
"""
@time:2020-07-06 19:12:26
@project:apiauto2020
@file:sessionHandler.py
@author:Jiang ChengLong
"""
from urllib import request
import requests

# 通过session，可以不需要手动去拿cookie信息，很有用
session=requests.sessions.session()

# 发送登录请求
login_res = session.post(url='http://*****/***/*/*/member/login',data={"mobilephone": "133***33331", "pwd": "12****"})

# 发送充值请求
login_res = request.post(
    url='http://*****/***/*/*/member/rech',
    data={"mobilephone": "133***33331", "pwd": "12****"})



