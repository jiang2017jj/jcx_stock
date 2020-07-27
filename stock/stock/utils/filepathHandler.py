# -*- coding = utf-8 -*-

import os

"""
Python中的os模块用于和系统进行交互，其中：
os.listdir()用于返回一个由文件名和目录名组成的列表，需要注意的是它接收的参数需要是一个 绝对的路径 。
os.path.isdir()用于判断对象是否为一个目录。
os.path.isfile()用于判断对象是否为一个文件。

"""
# 该文件所在的目录
current_path1 = os.path.dirname(__file__)
current_path2 = os.getcwd()
print(current_path1)
print(current_path2)

# 获取当前目录的上级目录
parent_path1 = os.path.abspath(os.path.dirname(current_path1))
parent_path2 = os.path.abspath(os.path.dirname(current_path2))
parent_path3 = os.path.abspath(os.path.join(os.getcwd(),'..'))
print(parent_path1)
print(parent_path2)
print(parent_path3)

# 获得某个路径的父级目录：
d = os.path.dirname(__file__)  # 返回当前文件所在的目录
# case_path = os.path.join(os.getcwd()) # 获取当前工作目录
# abspath = path.abspath(d) #返回d所在目录规范的绝对路径
parent_path = os.path.dirname(d)  # 获得d所在的目录,即d的父级目录
# parent_parent_path  = os.path.dirname(parent_path) #获得parent_path所在的目录即parent_path的父级目录
# 获取当前目录的上上级目录
parent_parent_path = os.path.abspath(os.path.join(os.getcwd(),'../..'))
print(parent_parent_path)

# 获取路径最后的文件夹名称或者文件名称
file_name = os.path.basename('/Users/jcl/Desktop/2020/python/python_all_0511/common')
print(file_name)
#该文件所在的绝对目录
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

# 多个参数链接
directories = os.path.join(os.getcwd(), 'clover', 'common', 'plugin')
print(directories)

# 作业:将目录下边的所有文件删除,包括文件夹

import os

def del_all(path):
    file_all = os.listdir(path)
    print(file_all)
    for file_name in file_all:
        file_path = os.path.join(path,file_name)
        print(file_path)
        # 如果是目录下的文件夹
        if os.path.isdir(file_path):
            print(file_path)
            # 递归调用，删除文件夹深处的文件
            del_all(file_path)
            # 然后删除文件夹
            os.rmdir(file_path)
        # 如果是文件，直接删除
        elif os.path.isfile(file_path):
            os.remove(file_path)

if __name__=="__main__":
    del_all("/Users/jcl/Desktop/11")

