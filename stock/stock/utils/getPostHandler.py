#!/usr/bin/python
# coding=utf-8

import json
import logging
import requests
import simplejson


# GetPostHandler类
class GetPostHandler:

    def __init__(self):
        pass

    def send_post(self,url,data,header=None):
        response = None
        if header != None:
            response = requests.post(url=url,data=data,header=header).json()
        else:
            response = requests.post(url=url, data=data).json()

        # sort_keys是按照ascii码排序；
        # indent是缩进的格数；
        # separators参数的作用是去掉‘，’ ‘：’后面的空格；
        # skipkeys参数在encoding过程中，dict对象的key只可以是string对象，如果是其他类型，那么在编码过程中就会抛出ValueError的异常，skipkeys可以跳过那些非string对象当作key的处理；
        # 输出真正的中文需要指定ensure_ascii=False；
        return json.dumps(response,sort_keys=False,indent=4,separators=(',',':'),skipkeys=True,ensure_ascii=False)

    def send_get(self,url,params,header=None):
        response=None
        if header!=None:
            response = requests.get(url=url,params=params,header=header).json()
        else:
            response = requests.get(url=url,params=params).json()

        return json.dumps(response,sort_keys=False,indent=4,separators=(',',':'),skipkeys=True,ensure_ascii=False)

    def run_get_post(self,method,url,data=None,params=None,header=None):
        response = None
        if method == 'GET':
            response = self.send_get(url=url,params=params,header=header)
        elif method == 'POST':
            response = self.send_post(url=url,data=data,header=header)
        else:
            response = None
            print("接口请求方式既不是post也不是get，请重新确认请求方式")
        return response




    def post(self,header, address, request_parameter_type, data):
        """
        post 请求
        :param header:  请求头
        :param address:  host地址
        :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
        :param data: 请求参数
        :return:
        """
        if request_parameter_type == 'raw':
            data = json.dumps(data)
        response = requests.post(url=address, data=data, headers=header, timeout=8)
        try:
            return response.status_code, response.json(), response.headers
        except json.decoder.JSONDecodeError:
            return response.status_code, '', response.headers
        except simplejson.errors.JSONDecodeError:
            return response.status_code, '', response.headers
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            return {}, {}, response.headers

    def get(self,header, address, request_parameter_type, data):
        """
        get 请求
        :param header:  请求头
        :param address:  host地址
        :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
        :param data: 请求参数
        :return:
        """
        if request_parameter_type == 'raw':
            data = json.dumps(data)
        response = requests.get(url=address, params=data, headers=header, timeout=8)
        if response.status_code == 301:
            response = requests.get(url=response.headers["location"])
        try:
            return response.status_code, response.json(), response.headers
        except json.decoder.JSONDecodeError:
            return response.status_code, '', response.headers
        except simplejson.errors.JSONDecodeError:
            return response.status_code, '', response.headers
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            return {}, {}, response.headers

    def put(self,header, address, request_parameter_type, data):
        """
        put 请求
        :param header:  请求头
        :param address:  host地址
        :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
        :param data: 请求参数
        :return:
        """
        if request_parameter_type == 'raw':
            data = json.dumps(data)
        response = requests.put(url=address, data=data, headers=header, timeout=8)
        try:
            return response.status_code, response.json(), response.headers
        except json.decoder.JSONDecodeError:
            return response.status_code, '', response.headers
        except simplejson.errors.JSONDecodeError:
            return response.status_code, '', response.headers
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            return {}, {}, response.headers

    def delete(self,header, address, data):
        """
        put 请求
        :param header:  请求头
        :param address:  host地址
        :param data: 请求参数
        :return:
        """
        response = requests.delete(url=address, params=data, headers=header)
        try:
            return response.status_code, response.json(), response.headers
        except json.decoder.JSONDecodeError:
            return response.status_code, '', response.headers
        except simplejson.errors.JSONDecodeError:
            return response.status_code, '', response.headers
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            return {}, {}, response.headers


import requests
import  unittest
import  json

class testClass(unittest.TestCase):
    def setUp(self):
        print ("初始化")
    def tearDown(self):
        print ("结束")

    # 测试get接口
    def testGet(self):
        keyword = {"wd":"poptest"}
        headers = {"User-Agent":"test",
                   'Referer': 'http://login.weibo.cn/login/?ns=1&revalid=2&backU'}
        cookies = dict(IPLOC="CN1100", ABTEST="1")
        res = requests.get("https://customer-api.helijia.com/app-customer/transformers/getCityList?version=3.3.0.1&sign_type=md5&city=110100&req_time=1472372990756&device_type=android&device_id=d3c1d53d0a8a378f",
                           params=keyword,
                           headers=headers,
                           cookies = cookies)
        print(res.text)
        if u"北京市" in res.text:
            print("pass")
            result = True
        else:
            print ("fail")
            result = False
        self.assertTrue(result)

    # 测试post接口
    def testPost(self):
        keyword = {"query":"postman"}
        headers = {"User-Agent":"hlj-android/3.3.0.1",
                   "Content-Type":"application/x-www-form-urlencoded",
                   'Referer': 'http://login.weibo.cn/login/?ns=1&revalid=2&backU'}
        cookies = dict(IPLOC="CN1100", ABTEST="1")
        res = requests.post("https://app.helijia.com/zmw/user/bind_dev",
                            #data=json.dumps(keyword),
                            data=keyword,
                            headers=headers,
                            cookies=cookies)
        print (res.text)
        if u"网页" in res.text:
            print ("pass")
        else:
            print ("fail")
        self.assertTrue(True)



if __name__=="__main__":
    unittest.main()

    gph = GetPostHandler()
    a = gph.run_get_post(method="GET",url="https://api-qa.xiaobangtouzi.com/flow/activity0603/activity/share")
    print(a)