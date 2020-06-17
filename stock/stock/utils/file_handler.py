# -*- coding = utf-8 -*-
"""
@time:2020-06-16 09:03:27
@project:stock
@file:file_handler.py
@author:Jiang ChengLong
"""
def allowed_file(filename):
    return  filename.rsplit('.', 1)[1].lower() in {'json','har'}