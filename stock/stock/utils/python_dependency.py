# -*- coding = utf-8 -*-
"""
@time:2020-06-16 09:01:49
@project:stock
@file:python_dependency.py
@author:Jiang ChengLong
"""
import os


def get_python_dependency():
    dependency = {}
    require = os.path.join(os.getcwd(), 'requirements.txt')
    with open(require) as file:
        lines = file.readlines()
        for line in lines:
            if '>=' in line:
                name, version = line.split('>=')
            else:
                name, version = line.split('==')
            name, version = name.strip(), version.strip()
            dependency.setdefault(name, version)
    return dependency