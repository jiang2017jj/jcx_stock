#!/usr/bin/env python3
#-*- coding = utf-8 -*-

"""
@time:2020-07-22 15:03:43
@project:python_all_0720
@file:fileHandler.py
@author:Jiang ChengLong
"""
import contextlib


# 正常我们使用open就能满足打开文件的功能，当然也可以自定义打开文件的这个操作
class MyOpen(object):

    def __init__(self, file_name):
        """初始化方法"""
        self.file_name = file_name
        self.file_handler = None

    def __enter__(self):
        """enter方法，返回file_handler"""
        print("enter方法:", self.file_name)
        self.file_handler = open(self.file_name, "r")
        return self.file_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit方法，关闭文件并返回True"""
        print("exit方法:", exc_type, exc_val, exc_tb)
        if self.file_handler:
            self.file_handler.close()
        return True

# 使用实例
with MyOpen("python_base.py") as file_in:
    for line in file_in:
        print(line)
        # 代码块中主动抛出一个除零异常，但整个程序不会引发异常
        raise ZeroDivisionError





# 内置库contextlib的使用
@contextlib.contextmanager
def open_func(file_name):
    # __enter__方法
    print("open file:", file_name, "in __enter__")
    file_handler = open(file_name, "r")

    yield file_handler

    # __exit__方法
    print("close file:", file_name, "in __exit__")
    file_handler.close()
    return

# 使用实例
with open_func("python_base.py") as file_in:
    for line in file_in:
        print(line)
        break



# 内置库contextlib的使用
class MyOpen2(object):

    def __init__(self, file_name):
        """初始化方法"""
        self.file_handler = open(file_name, "r")
        return

    def close(self):
        """关闭文件，会被自动调用"""
        print("call close in MyOpen2")
        if self.file_handler:
            self.file_handler.close()
        return

# 使用实例
with contextlib.closing(MyOpen2("python_base.py")) as file_in:
    pass



# 主要是讲readline()和readlines()的区别，readlines读取到的是所有行组成的列表，readline读取的是文件中的一行
def count_avg_time2():
    try:
        list_last_column = []
        total = 0
        avg = 0
        with open("jcl.log", "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = [i for i in line.split()]
                if not line:
                    break
                list_last_column.append(float(line[-1]))
        # return list_last_column
        if list_last_column:
            for i in list_last_column:
                total = total + i
            avg = total / len(list_last_column)
        return avg

    except Exception as e:
        print(e)


def count_avg_time3():
    try:
        list_last_column = []
        total = 0
        avg = 0
        with open("jcl.log", "r", encoding="utf-8") as f:
            while True:
                # 这是readline()
                lines = f.readline()
                # print(f.readlines())
                # print(type(lines))
                if not lines:
                    break
                item = [i for i in lines.split()]
                list_last_column.append(float(item[-1]))

        if list_last_column:
            for i in list_last_column:
                total = total + i
            avg = total / len(list_last_column)
        return avg

    except Exception as e:
        print(e)


if __name__ == "__main__":

    # avg_time2 = count_avg_time2()
    # print(avg_time2)

    avg_time3 = count_avg_time3()
    print(avg_time3)