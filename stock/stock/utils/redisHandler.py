# -*- coding = utf-8 -*-

import time
import redis
from sshtunnel import SSHTunnelForwarder

from config import REDIS_SSHFLAG, REDIS_SSH_JUMP_HOST, REDIS_SSH_JUMP_PORT, REDIS_LOCAL_SSH_USERNAME, \
    REDIS_LOCAL_SSH_PASSWORD, REDIS_LOCAL_SSH_PKEYPATH, redis_jump_dict, redis_direct_dict
from handlers.logHandler import Jcl_Logger


class RedisHandler():

    def __init__(self):
        # 等待异步连接服务时间，单位：秒
        self.timeToWaitRemoteRedis = 2
        self.redis_conn = self.connect_redis_DB(withSSH=REDIS_SSHFLAG)

    # 登陆到热地说机器：通过跳板机+不通过跳板机
    def connect_redis_DB(self,withSSH=REDIS_SSHFLAG):
        try:
            if withSSH:
                server = SSHTunnelForwarder(
                    (REDIS_SSH_JUMP_HOST,REDIS_SSH_JUMP_PORT),
                    ssh_username=REDIS_LOCAL_SSH_USERNAME,  # 链接跳板机用户名
                    ssh_password=REDIS_LOCAL_SSH_PASSWORD,  # 私钥中的密码
                    ssh_pkey=REDIS_LOCAL_SSH_PKEYPATH,
                    remote_bind_address=(redis_jump_dict['host'], redis_jump_dict['port'])  # 数据库机器的配置
                )

                server.start()

                Jcl_Logger('jcllogger').getlog().debug("server开启")

                time.sleep(self.timeToWaitRemoteRedis)

                # 此处的host必须为127.0.0.1
                Jcl_Logger('jcllogger').getlog().debug("使用跳板机登陆redis服务器")

                return redis.Redis(host='127.0.0.1',port=server.local_bind_port,db=redis_jump_dict['db'])

            else:
                Jcl_Logger('jcllogger').getlog().debug("不使用跳板机登陆redis服务器")

                # 可以使用连接池进行建立redis连接
                # pool = redis.ConnectionPool(**redis_direct_dict)
                # r = redis.Redis(connection_pool=pool)

                return redis.Redis(**redis_direct_dict)

        except Exception as e:
            Jcl_Logger('jcllogger').getlog().debug("登陆redis服务器失败:{}".format(e))



    #设置redis中数据库某个键对应的值
    def setRedisKeyDB(self,key,value):
        pass

    # 删除redis中数据库的某个键
    def deleteRedisKeyDB(self,keyName, param,db=0):
        r = self.connect_redis_DB(**redis_direct_dict)
        key = keyName + str(param)
        resultDel = r.delete(key)
        return resultDel

    # 删除redis中数据库某个键,在服务器上执行，不需要走redisConnect方法
    def deleteserverRedisKeyDB(self,keyName,param):
        r=self.redis.Redis(**redis_direct_dict)
        key = keyName + str(param)
        resultDel = r.delete(key)
        return resultDel

    #获取redis中数据库某个键对应的值
    def updateRedisKeyDB(self,mobile):
        pass

    #获取redis中数据库某个键对应的值
    def queryVerifyCodeRedisKeyDB1(self,mobile):
        r = self.connect_redis_DB(**redis_direct_dict)
        key = 'sms:codeByMobile:' + str(mobile)
        return r.get(key)

if __name__=="__main__":
    rh = RedisHandler()
    rh.connect_redis_DB()
    a=rh.queryVerifyCodeRedisKeyDB1("15801505179")
    print(a)