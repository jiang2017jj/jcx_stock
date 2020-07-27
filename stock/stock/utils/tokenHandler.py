#!/usr/bin/env python
# coding=utf-8

import requests
import json
from config import token_url, token_headers, token_request_param

class tokenHandler(object):
    def __init__(self):
        pass

    #通过接口获取token
    def get_token(self):
        try:
            res = requests.post(url=token_url,data=json.dumps(token_request_param),headers=token_headers)
            if res:
                return res.json()["data"]["token"]
        except Exception as error:
            # print('没有生成token，报错信息如下：',error)

            return None
            # flask框架下的jsonify有时候也不方便
            # return jsonify({
            #     'status': 500,
            #     'message': u'获取token失败，请检查获取token接口的链接以及参数',
            #     'data': {
            #         'error': str(error)
            #     }
            # })

if __name__=="__main__":
    th = tokenHandler()
    a = th.get_token()
    print(a)

