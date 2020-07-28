# -*- coding = utf-8 -*-
"""
@time:2020-07-02 18:45:49
@project:apiauto2020
@file:jsonHandler.py
@author:Jiang ChengLong
"""
import json
import os

'''
dict['key']只能获取存在的值，如果不存在则触发KeyError
dict.get(key, default=None)，返回指定键的值，如果值不在字典中返回默认值None
excel文件中请求数据有可能为空，所以用get方法获取
'''

# 找到测试结果存储的目录testresults
htmlresult_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testresults')

#处理json文件
class JsonHandler(object):
    def __init__(self,file_path):
        self.file_path = os.path.join(self.file_path,'jsonfiles')
        self.data = self.read_data() #read_data函数需要定义

    # 根据关键字获取数据
    def get_data(self,key):
        # return self.data[key]
        return self.data.get(key)

    # 将cookies数据写入json文件
    def write_data(self, data):
        with open('../dataconfig/cookie.json', 'w') as fp:
            fp.write(json.dumps(data))

    # 定义read_data方法,读取json文件
    def read_data(self,jsonname):
        with open(os.path.join(self.file_path,jsonname),'r', encoding='utf-8') as f:
            contents_str = f.read()
            contents_dict = json.load(contents_str)  #json.loads()函数是将字符串转化为字典；json.dumps()函数是将字典转化为字符串
            contents_dict_values = list(contents_dict.values())
            return contents_dict_values


    # 将数据写入json文件
    def write_data(self,file_path,newdata):
        #将data写入jsonfile
        #file_path = 'D:\\APIinterfacetest\\apiauto\datafile\\cookie.json'
        with open(file_path,'wb') as fp:
            fp.write(json.dumps(newdata))


    def create_json(self,api_id, api, data):
        """
        根据json数据生成关联数据接口
        :param api_id: 接口ID
        :param data: Json数据
        :param api: 格式化api数据
        :return:
        """
        # 用来mock数据？
        if isinstance(data, dict):
            for i in data:
                m = (api + "[\"%s\"]" % i)
                # AutomationResponseJson(automationCaseApi=api_id, name=i, tier=m, type='json').save()
                self.create_json(api_id, m, data[i])

    def check_json(self,src_data, dst_data):
        """
        校验的json
        :param src_data:  校验内容
        :param dst_data:  接口返回的数据（被校验的内容
        :return:
        """
        global result
        try:
            if isinstance(src_data, dict):
                """若为dict格式"""
                for key in src_data:
                    if key not in dst_data:
                        result = 'fail'
                    else:
                        # if src_data[key] != dst_data[key]:
                        #     result = False
                        this_key = key
                        """递归"""
                        if isinstance(src_data[this_key], dict) and isinstance(dst_data[this_key], dict):
                            self.check_json(src_data[this_key], dst_data[this_key])
                        elif isinstance(type(src_data[this_key]), type(dst_data[this_key])):
                            result = 'fail'
                        else:
                            pass
                return result
            return 'fail'

        except Exception as e:
            return 'fail'




# 字典转换成json，即：将其他数据转换成json
def to_json(data):
    try:
        # data参数竟然可以是列表，但是返回的肯定不是json了，想返回json字符串，则dumps（）必须传入的是字典对象
        json_file = json.dumps(data)
        return json_file
    except Exception as e:
        print(e)

# 将json转换成其他对象，如字典
def json_to_other(json_data):
    try:
        other_file = json.loads(json_data)
        return other_file
    except Exception as e:
        print(e)


# json.load()是从json文件中读取数据，格式是dict
def read_json(file_path):
    with open(file_path,'r') as f:
        data = json.load(f)
        return data

# json.dump()是用来把一个序列化对象，一般是字典，转化为一个JSON格式流，然后写入指定的文件中去
def write_json(file_path,w_data):
    with open(file_path,'w') as f:
        data = json.dump(w_data,f)
        return data


if __name__ == "__main__":
    dict_data = {
        'jcl': 'tester',
        'jcx': 'dev',
        'ztt': 'pm'
    }
    # 列表数据也不会报错，但是用在这就没必要了
    other_data = [1, 2, 3]
    # print(to_json(dict_data))
    # print(to_json(other_data))
    # print(type(to_json(other_data)))

    json_data = '{"jcl": "tester", "jcx": "dev", "ztt": "pm"}'
    print(type(json_data))
    print(json_to_other(json_data))
    print(type(json_to_other(json_data)))


    jsonhandler = JsonHandler()
    #a是一个dict
    a= jsonhandler.read_data()
    print(a)
    print(a.get("type"))



