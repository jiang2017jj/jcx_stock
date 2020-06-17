# -*- coding = utf-8 -*-
"""
@time:2020-06-16 09:02:36
@project:stock
@file:nodejs_dependency.py
@author:Jiang ChengLong
"""
import json
import os


def get_nodejs_dependency():
    require = os.path.join(os.getcwd(), 'package.json')
    with open(require) as file:
        data = json.load(file)
        dependency = {**data['dependencies'], **data['devDependencies']}
    return dependency