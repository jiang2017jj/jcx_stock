# -*- coding = utf-8 -*-
"""
@time:2020-07-06 18:36:31
@project:apiauto2020
@file:exceptionHandler.py
@author:Jiang ChengLong
"""
from rest_framework.views import exception_handler


class exceptionHandler():
    def __init__(self):
        pass

    def custom_exception_handler(self,exc,context):
        # Call REST framework's default exception handler first,
        # to get the standard error response.
        response = exception_handler(exc,context)
        # Now add the HTTP status code to the response.
        if response is not None:
            try:
                response.data['code'] = response.status_code
                response.data['msg'] = response.data['detail']
                # response.data['data'] = None #可以存在
                # 删除detail字段
                del response.data['detail']
            except KeyError:
                for k, v in dict(response.data).items():
                    if v == ['无法使用提供的认证信息登录。']:
                        if response.status_code == 400:
                            response.status_code = 200
                        response.data = {}
                        response.data['code'] = '999984'
                        response.data['msg'] = '账号或密码错误'
                    elif v == ['该字段是必填项。']:
                        if response.status_code == 400:
                            response.status_code = 200
                        response.data = {}
                        response.data['code'] = '999996'
                        response.data['msg'] = '参数有误'

        return response


if __name__=="__main__":
    # 进行异常自定义
    eh = exceptionHandler()
    # eh.custom_exception_handler()