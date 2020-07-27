#!/usr/bin/python
# coding=utf-8


import subprocess

'''
执行一个外部脚本命令，参数为命令行，如arg="sudo php /data/utils/flushmem.php -h10.9.116.177 -p11211"
subprocess模块：https://blog.csdn.net/chengxuyuanyonghu/article/details/79317772     
'''

class scriptHandler():

    def __init__(self,arg):
        self.arg = arg

    # 执行外部脚本，参数为命令行
    def callScript(self):
        proc = subprocess.Popen(self.arg,shell=True,stdout=subprocess.PIPE)
        script_response = proc.stdout.read()
        return script_response


if __name__ == "__main__":
    arg = "pwd"
    sh = scriptHandler(arg)
    a = sh.callScript()
    print(a)