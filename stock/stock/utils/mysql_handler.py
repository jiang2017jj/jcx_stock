# -*- coding = utf-8 -*-
"""
@time:2020-06-16 09:00:38
@project:stock
@file:mysql_handler.py
@author:Jiang ChengLong
"""
def get_mysql_error(error):
    """
    :param error:
    :return:
    """
    # (pymysql.err.ProgrammingError) (1146, "Table 'clover.suite' doesn't exist")
    error = error.args[0]
    error = error.strip("(pymysql.err.ProgrammingError) (").strip(")")
    return tuple(error.split(","))
