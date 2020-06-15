# -*- coding = utf-8 -*-
"""
@time:2020-06-15 22:44:46
@project:stock
@file:task_jobs.py
@author:Jiang ChengLong
"""

# 新的定时任务只需要去app.config中进行配置即可
# 主要用于定期获取一些数据

# 测试用的定时任务
def job_1():
  print("JCL调试定时任务")
