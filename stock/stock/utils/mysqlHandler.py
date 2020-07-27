#!/usr/bin/python
# coding=utf-8

"""
@time:2020-07-02 17:38:14
@project:apiauto2020
@file:mysqlHandler.py
@author:Jiang ChengLong
"""
import time
import pymysql
from sshtunnel import SSHTunnelForwarder
import config
from config import mysql_direct_dict,mysql_jump_dict


# mysql类
from handlers.logHandler import Jcl_Logger


class MysqlHandler():

    def __init__(self):
        self.timeToWaitRemoteDB = 1  # 等待异步连接服务时间，单位s秒
        self.conn = self.connectDB(withSSH=config.SSHFLAG)

    # 连接数据库,分为是否通过跳板机
    def connectDB(self,withSSH=config.SSHFLAG):
        self.conn = None
        self.server = None
        self.withSSH = withSSH
        try:
            # 通过跳板机登录数据库，需要持续优化，暂时用不上
            if withSSH:
                # 制定ssh登录的跳板机的地址和端口号
                self.server = SSHTunnelForwarder(
                    (config.SSH_JUMP_HOST, config.SSH_JUMP_PORT),  # 跳板机机器的配置
                    ssh_host_key=None,
                    ssh_username=config.LOCAL_SSH_USERNAME,  # 链接跳板机用户名
                    ssh_password=config.LOCAL_SSH_PASSWORD,  # 私钥中的密码
                    ssh_pkey=config.LOCAL_SSH_PKEYPATH,
                    remote_bind_address=(mysql_jump_dict['host'],mysql_jump_dict['port']))  # 数据库机器的配置
                self.server.start()
                time.sleep(self.timeToWaitRemoteDB)
                # host有的公司需要必须为host='127.0.0.1'，具体情况具体分析
                self.conn = pymysql.connect(host='127.0.0.1', port=self.server.local_bind_port, **mysql_jump_dict)
            else:
                # 不需要跳板机，直接登录数据库的情况
                self.conn = pymysql.connect(**mysql_direct_dict)

            return self.conn

        except Exception as e:
            print(e)
            return None


    # 关闭数据库的连接
    def closeDB(self):
        pass

    # 封装对mysql的操作方法，参数为增删该查关键字和具体的sql语句
    def executeSql(self,command,sql):
        command = command.strip()
        sql = sql.encode('utf-8')
        try:
            cursor = self.conn.cursor()
            if command in ('SELECT','select'):
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
            elif command in ('insert', 'INSERT','delete', 'DELETE', 'update', 'UPDATE'):
                try:
                    cursor.execute(sql)
                    self.conn.commit()
                    Jcl_Logger('jcllogger').getlog().debug("操作成功")
                except Exception as e:
                    self.conn.rollback()
                    Jcl_Logger('jcllogger').getlog().debug("{}操作失败，事务回滚".format(command))
            else:
                Jcl_Logger('jcllogger').getlog().debug("{}不是mysql增删改查命令，请重新检查command参数".format(command))

        except Exception as e:
            Jcl_Logger('jcllogger').getlog().debug("{}:{}sql语句执行失败，请检查executeSql方法,报错信息:{}".format(command,str(sql),e))

        finally:
            self.conn.close()

if __name__ == "__main__":

    dbhandler = MysqlHandler()

    insert_data = dbhandler.executeSql("isnert","insert jcl_tbl_new values(null,'jcl7',44,'2020-09-09','jcl','w','cats')")

    # delete_data = dbhandler.executeSql("delete","delete from jcl_tbl_new where name = 'jcl2'")

    # update_data = dbhandler.executeSql("update","update jcl_tbl_new set age=200 where name = 'jcl1'")

    # select_data=dbhandler.executeSql("select","select * from jcl_tbl_new")
    # print(select_data)

    # select_data=dbhandler.executeSql("qABSOLUTE","select * from jcl_tbl_new")

    # select_data = dbhandler.executeSql("select", "selectwwwwww * from jcl_tbl_new")



