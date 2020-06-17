# -*- coding = utf-8 -*-
"""
@time:2020-06-16 09:04:05
@project:stock
@file:json handler.py
@author:Jiang ChengLong
"""
import datetime
import json


class StockJSONEncoder(json.JSONEncoder):

    def default(self, data):
        if isinstance(data, datetime.datetime):
            return data.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, data)