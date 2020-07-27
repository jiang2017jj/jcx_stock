#!/usr/bin/env python3
#-*- coding = utf-8 -*-

import random
import time
from queue import Queue
from threading import Thread
from redis import redis

# 异步任务 需要搞定，celery和redis分别实现待完善


# 生产者、消费者例子
def consumer():         # 定义消费者，由于有yeild关键词，此消费者为一个生成器
    print("[Consumer] Init Consumer ......")
    r = "init ok"       # 初始化返回结果，并在启动消费者时，返回给生产者
    while True:
        n = yield r     # 消费者通过yield关键词接收生产者产生的消息，同时返回结果给生产者
        print("[Consumer] conusme n = %s, r = %s" % (n, r))
        r = "consume %s OK" % n     # 消费者消费结果，下个循环返回给生产者


def produce(c):         # 定义生产者，此时的 c 为一个生成器
    print("[Producer] Init Producer ......")
    r = c.send(None)    # 启动消费者生成器，同时第一次接收返回结果
    print("[Producer] Start Consumer, return %s" % r)
    n = 0
    while n < 5:
        n += 1
        print("[Producer] While, Producing %s ......" % n)
        r = c.send(n)   # 向消费者发送消息，同时准备接收结果。此时会切换到消费者执行
        print("[Producer] Consumer return: %s" % r)
    c.close()           # 关闭消费者生成器
    print("[Producer] Close Producer ......")

# produce(consumer())


# ======================================================================================================================
def customer():
    r = ''
    while True:
        n = yield r
        print('[CUSTOMER]第%s次吃鸡翅，超级开心' % n)


def product(customer):
    # 生产者
    customer.__next__()
    n = 1
    while n < 5:
        print('[PRODUCT]第%s次做鸡翅' % n)
        # 引入消费者来消费
        customer.send(n)
        print('[PRODUCT]第%s次卖完了，重新去生产' % n)
        n += 1
    customer.close()

# ======================================================================================================================

queue = Queue(10)

class Producer(Thread):
    def run(self):
        while True:
            elem = random.randrange(9)
            queue.put(elem)
            print("厨师 {} 做了 {} 饭 --- 还剩 {} 饭没卖完".format(self.name, elem, queue.qsize()))
            time.sleep(random.random())

class Consumer(Thread):
    def run(self):
        while True:
            elem = queue.get()
            print ("吃货{} 吃了 {} 饭 --- 还有 {} 饭可以吃".format(self.name, elem, queue.qsize()))
            time.sleep(random.random())

#
# def consumer():
#     r = ''
#     while True:
#         n = yield r
#         if not n:
#             return
#         print("producer is running:{}".format(n))
#         r = '200 OK'
#
# def producer(c):
#     c.send(None)
#     n=0
#     while n<5:
#         n=n+1
#         print("producer is running:{}".format(n))
#         r = c.send(n)
#         print("consumer return:{}".format(r))
#     c.close()
#
# c = consumer()
# producer(c)


def main():
    for i in range(3):
        p = Producer()
        p.start()
    for i in range(2):
        c = Consumer()
        c.start()



class Task(object):

    def __init__(self):

        self.rcon = redis.StrictRedis(host='localhost', db=5)
        self.ps = self.rcon.pubsub()
        self.ps.subscribe('task:pubsub:channel')

    def listen_task(self):
        for i in self.ps.listen():
            if i['type'] == 'message':
                print ("Task get", i['data'])




if __name__ == '__main__':

    customer = customer()
    product(customer)


    print ('listen task channel')
    Task().listen_task()


    main()


