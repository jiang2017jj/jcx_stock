# -*- coding = utf-8 -*-
"""
@time:2020-07-02 19:15:55
@project:apiauto2020
@file:testdataHandler.py
@author:Jiang ChengLong
"""
import json

from handlers.excelHandler import ExcelHandler
from handlers.getPostHandler import GetPostHandler


class global_var:
    Id = '0'
    name = '1'
    url = '2'
    run = '3'
    request_method = '4'
    request_header = '5'
    case_depend = '6'
    data_depend = '7'
    field_depend = '8'
    request_data = '9'
    expect = '10'
    result = '11'


class GetDependentData:

    def __init__(self,tablename,depend_case_id,case_id,depend_key):
        # 被依赖的case_id
        self.case_id = case_id
        # 依赖别人的case_id
        self.depend_case_id = depend_case_id
        # 依赖别人的key
        self.depend_key = depend_key
        self.oper_excel = ExcelHandler()
        self.tablename = tablename
        self.get_post = GetPostHandler()

    # 通过case_id去获取依赖case_id的整行数据
    def get_case_line_data(self):
        rows_data = self.oper_excel.readOneRow(self.tablename,self.case_id,sheetIndex=0)
        return rows_data

    #执行依赖测试，获取结果
    def run_dependent(self):
        url=''
        method=''
        header=''
        request_data=''
        data = self.get_case_line_data()
        if data:
            url = data[global_var.url]
            method = data[global_var.request_method]
            header = data[global_var.request_header]
            request_data = data[global_var.request_data]
        res = self.get_post.run_get_post(method=method,url=url,data=request_data,header=header,params=request_data)
        return res

    #获取依赖字段的响应数据：通过执行依赖测试case来获取响应数据，响应中某个字段数据作为依赖key的value
    def get_value_for_key(self):
        #执行依赖case返回结果
        response_data = self.run_dependent()
        response_data_dict = json.loads(response_data)
        print(response_data)
        for key,val in response_data_dict.items:
            if key == self.depend_key:
                depend_key_value = response_data_dict[key]
        return depend_key_value


class GetData:

    def __init__(self,tablename):
        self.oper_excel = ExcelHandler()
        self.tablename = tablename

    #去获取excel行数，就是case个数
    def get_case_lines(self,index=0):
        return self.oper_excel.get_table_and_open(self.tablename).sheets[index].nrows

    #获取是否执行
    def get_is_run(self,row):
        flag = None
        col = int(global_var.run)
        run_model = self.oper_excel.readCell(self.tablename,row,col)
        if run_model == 'yes':
            flag = True
        else:
            flag = False
        return flag

    #获取请求方式
    def get_request_method(self,row):
        col = int(global_var.request_method)
        request_method = self.oper_excel.readCell(self.tablename,row,col)
        return request_method

    #获取url
    def get_request_url(self,row):
        col = int(global_var.url)
        url = self.oper_excel.readCell(self.tablename,row,col)
        return url

    # 获取请求头header
    def get_request_header(self,row):
        col = int(global_var.request_header)
        data = self.oper_excel.readCell(self.tablename,row,col)
        if data == '':
            return None
        else:
            return data
    # 通过获取头关键字拿到data数据
    def get_header_value(self, row):
        pass


    #获取请求数据
    def get_request_data(self,row):
        col = int(global_var.request_data)
        data = self.oper_excel.readCell(self.tablename,row,col)
        if data == '':
            return None
        return data

    #通过获取请求关键字拿到data数据
    def get_data_value(self,row):
        pass


    # 获取预期结果
    def get_expect_data(self,row):
        col = int(global_var.expect)
        expect = self.oper_excel.readCell(row,col)
        return expect

    # 写入数据
    def write_result(self,row,value):
        col = int(global_var.result)
        self.oper_excel.writeToExcel(row,col,value)

    #获取依赖数据的key
    def get_depend_key(self,row):
        col = int(global_var.data_depend)
        depend_key = self.oper_excel.readCell(self.tablename,row,col)
        if depend_key == '':
            return None
        else:
            return depend_key

    #判断是否有case依赖
    def is_depend(self,row):
        col = int(global_var.case_depend)
        depend_case_id = self.oper_excel.readCell(self.tablename,row,col)
        if depend_case_id == '':
            return None
        else:
            return depend_case_id

    #获取请求依赖字段
    def get_depend_field(self,row):
        col = int(global_var.field_depend)
        data = self.oper_excel.readCell(self.tablename,row,col)
        if data == '':
            return None
        else:
            return data



if __name__=="__main__":
    # 具体使用时再进行完善
    gdd = GetDependentData('interface.xls','test01')
    res = gdd.run_dependent()
    print(res)


