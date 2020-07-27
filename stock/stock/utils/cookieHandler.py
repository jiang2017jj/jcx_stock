#!/usr/bin/env python
# coding=utf-8

import json
import requests

class CookieHandler(object):

    def __init__(self):
        pass

    def get_cookie(self):
        url = "https://account.xiaobangtouzi.com/account/login"
        headers = {'Content-Type':'application/json','App-Id':'wxfc4b19a1283a4725'}
        request_param = {
            "phone": "15811033103",
            "code": "180326"
        }
        response = requests.post(url,data=json.dumps(request_param),headers=headers)
        return response.json()["data"]["cookies"]

if __name__=="__main__":
    # 获取cookie,还不知道怎么产生cookie,后续更新
    ch = CookieHandler()
    a=ch.get_cookie()
    print(a)