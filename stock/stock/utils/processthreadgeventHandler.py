#!/usr/bin/env python3
#-*- coding = utf-8 -*-

import asyncio
import re
import threading
import aiohttp
import json
from pymongo import MongoClient
import glob
import os
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from PIL import Image
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from random import randint
# from example15 import is_prime
import multiprocessing
from multiprocessing import Process
import random
from multiprocessing.pool import Pool
import subprocess
import greenlet
import gevent
import requests
# gevent是切换协程用的
from gevent import monkey
monkey.patch_all()

"""
扩展性系统性能
- 垂直扩展 - 增加单节点处理能力
- 水平扩展 - 将单节点变成多节点（读写分离/分布式集群）
并发编程 - 加速程序执行 / 改善用户体验
耗时间的任务都尽可能独立的执行，不要阻塞代码的其他部分
- 多线程
1. 创建Thread对象指定target和args属性并通过start方法启动线程
2. 继承Thread类并重写run方法来定义线程执行的任务
3. 创建线程池对象ThreadPoolExecutor并通过submit来提交要执行的任务
第3种方式可以通过Future对象的result方法在将来获得线程的执行结果
也可以通过done方法判定线程是否执行结束
- 多进程
- 异步I/O
"""


# class ThumbnailThread(Thread):

#     def __init__(self, infile):
#         self.infile = infile
#         super().__init__()

#     def run(self):
#         file, ext = os.path.splitext(self.infile)
#         filename = file[file.rfind('/') + 1:]
#         for size in (32, 64, 128):
#             outfile = f'thumbnails/{filename}_{size}_{size}.png'
#             image = Image.open(self.infile)
#             image.thumbnail((size, size))
#             image.save(outfile, format='PNG')


def gen_thumbnail(infile):
    file, ext = os.path.splitext(infile)
    filename = file[file.rfind('/') + 1:]
    for size in (32, 64, 128):
        outfile = f'thumbnails/{filename}_{size}_{size}.png'
        image = Image.open(infile)
        image.thumbnail((size, size))
        image.save(outfile, format='PNG')


# def main():
#     start = time.time()
#     threads = []
#     for infile in glob.glob('images/*'):
#         # t = Thread(target=gen_thumbnail, args=(infile, ))
#         t = ThumbnailThread(infile)
#         t.start()
#         threads.append(t)
#     for t in threads:
#         t.join()
#     end = time.time()
#     print(f'耗时: {end - start}秒')


def main():
    pool = ThreadPoolExecutor(max_workers=30)
    futures = []
    start = time.time()
    for infile in glob.glob('images/*'):
        # submit方法是非阻塞式的方法
        # 即便工作线程数已经用完，submit方法也会接受提交的任务
        future = pool.submit(gen_thumbnail, infile)
        futures.append(future)
    for future in futures:
        # result方法是一个阻塞式的方法 如果线程还没有结束
        # 暂时取不到线程的执行结果 代码就会在此处阻塞
        future.result()
    end = time.time()
    print(f'耗时: {end - start}秒')
    # shutdown也是非阻塞式的方法 但是如果已经提交的任务还没有执行完
    # 线程池是不会停止工作的 shutdown之后再提交任务就不会执行而且会产生异常
    pool.shutdown()


"""
线程间通信（共享数据）非常简单因为可以共享同一个进程的内存
进程间通信（共享数据）比较麻烦因为操作系统会保护分配给进程的内存
要实现多进程间的通信通常可以用 系统管道、套接字、三方服务 来实现
multiprocessing.Queue
守护线程 - daemon thread
守护进程 - firewalld / httpd / mysqld
在系统停机的时候不保留的进程 - 不会因为进程还没有执行结束而阻碍系统停止
"""
def output(content):
    while True:
        print(content, end='')


def main():
    Thread(target=output, args=('Ping', ), daemon=True).start()
    Thread(target=output, args=('Pong', ), daemon=True).start()
    sleep(5)
    print('bye!')


"""
多个线程竞争一个资源 - 保护临界资源 - 锁（Lock/RLock）
多个线程竞争多个资源（线程数>资源数） - 信号量（Semaphore）
多个线程的调度 - 暂停线程执行/唤醒等待中的线程 - Condition
"""
class Account():
    """银行账户"""

    def __init__(self, balance=0):
        self.balance = balance
        lock = threading.Lock()
        self.condition = threading.Condition(lock)

    def withdraw(self, money):
        """取钱"""
        with self.condition:
            while money > self.balance:
                self.condition.wait()
            new_balance = self.balance - money
            sleep(0.001)
            self.balance = new_balance

    def deposit(self, money):
        """存钱"""
        with self.condition:
            new_balance = self.balance + money
            sleep(0.001)
            self.balance = new_balance
            self.condition.notify_all()


def add_money(account):
    while True:
        money = randint(5, 10)
        account.deposit(money)
        print(threading.current_thread().name,
              ':', money, '====>', account.balance)
        sleep(0.5)


def sub_money(account):
    while True:
        money = randint(10, 30)
        account.withdraw(money)
        print(threading.current_thread().name,
              ':', money, '<====', account.balance)
        sleep(1)


def main():
    account = Account()
    with ThreadPoolExecutor(max_workers=10) as pool:
        for _ in range(5):
            pool.submit(add_money, account)
            pool.submit(sub_money, account)


"""
多进程和进程池的使用
多线程因为GIL的存在不能够发挥CPU的多核特性
对于计算密集型任务应该考虑使用多进程
time python3 example22.py
real    0m11.512s
user    0m39.319s
sys     0m0.169s
"""
import concurrent.futures
import math

PRIMES = [
    1116281,
    1297337,
    104395303,
    472882027,
    533000389,
    817504243,
    982451653,
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419
] * 5


def is_prime(n):
    """判断素数"""
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def main():
    """主函数"""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))



# 协程（coroutine）- 可以在需要时进行切换的相互协作的子程序
def num_generator(m, n):
    """指定范围的数字生成器"""
    yield from range(m, n + 1)


async def prime_filter(m, n):
    """素数过滤器"""
    primes = []
    for i in num_generator(m, n):
        if is_prime(i):
            print('Prime =>', i)
            primes.append(i)

        await asyncio.sleep(0.001)
    return tuple(primes)


async def square_mapper(m, n):
    """平方映射器"""
    squares = []
    for i in num_generator(m, n):
        print('Square =>', i * i)
        squares.append(i * i)

        await asyncio.sleep(0.001)
    return squares


def main():
    """主函数"""
    loop = asyncio.get_event_loop()
    future = asyncio.gather(prime_filter(2, 100), square_mapper(1, 100))
    future.add_done_callback(lambda x: print(x.result()))
    loop.run_until_complete(future)
    loop.close()


# ===================================================================================
# python_thread_multiprocee.py by xianhu
# 定义全局变量Queue
g_queue = multiprocessing.Queue()
g_search_list = list(range(10000))

# 定义一个IO密集型任务：利用time.sleep()
def task_io(task_id):
    print("IOTask[%s] start" % task_id)
    while not g_queue.empty():
        time.sleep(1)
        try:
            data = g_queue.get(block=True, timeout=1)
            print("IOTask[%s] get data: %s" % (task_id, data))
        except Exception as excep:
            print("IOTask[%s] error: %s" % (task_id, str(excep)))
    print("IOTask[%s] end" % task_id)
    return


# 定义一个计算密集型任务：利用一些复杂加减乘除、列表查找等
def task_cpu(task_id):
    print("CPUTask[%s] start" % task_id)
    while not g_queue.empty():
        count = 0
        for i in range(10000):
            count += pow(3*2, 3*2) if i in g_search_list else 0
        try:
            data = g_queue.get(block=True, timeout=1)
            print("CPUTask[%s] get data: %s" % (task_id, data))
        except Exception as excep:
            print("CPUTask[%s] error: %s" % (task_id, str(excep)))
    print("CPUTask[%s] end" % task_id)
    return task_id


def init_queue():
    print("init g_queue start")
    while not g_queue.empty():
        g_queue.get()
    for _index in range(10):
        g_queue.put(_index)
    print("init g_queue end")
    return



# 进程类
class My_Process():
    def __init__(self):
        pass

    def process_1(self):
        # 这个只是在开启一个进程，并且拿到进程id
        print('启动一个进程，这是一个进程ID：{}'.format(os.getpid()))

        # pid_main是主进程，所以返回到时候父进程返回了一个子进程id，子进程返回了一个0
        # 主进程不一定是父进程，也可能是子进程
        pid_main = os.fork()
        print('打开主进程{}'.format(pid_main))

        sleep(2)

        if pid_main == 0:
            print("{}是一个子进程，我的父进程是：{}".format(os.getpid(), os.getppid()))
            sleep(1)
        else:
            print("{}是一个父进程，我的子进程是：{}".format(os.getpid(), pid_main))
            sleep(1)


    def run_proc(self,name):
        print("run child process {},name is {}".format(os.getpid(),name))


    def long_time_task(self,name):
        print('进程名字：{name}，获取的pid:{pid}'.format(name=name,pid=os.getpid()))
        start = time.time()
        time.sleep(random.random()*3)
        end = time.time()
        print('进程名字：{0}，进程运行时间为:{1}'.format(name,end-start))


    def create_nslookup(self):
        # 模拟命令行nslookup www.python.org
        r = subprocess.call(['nslookup','www.python.org'])
        print(r)
        # 如果子进程需要输入
        p = subprocess.Popen(['nslookup'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p.communicate(b'set q=mx\npython.org\nexit\n')
        print(output.decode('utf-8'))
        print(p.returncode)



class My_Thread():
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    # 不知道咋用
    def run_thread(self,n):
        for i in range(100000):
            self.lock.acquire()
            try:
                #进行修改动作
                pass

            finally:
                self.lock.release()

    # 线程
    def my_thread(self):
        print('my_thread中threading {} is running......'.format(threading.current_thread().name))
        n = 0
        while n<5:
            n=n+1
            print('thread {} >>>>{}'.format(threading.current_thread().name,n))
            time.sleep(1)
        print('my_thread中的thread {} ended......'.format(threading.current_thread().name))



# 验证aiohttp模块是正常使用的
class Test_Aiohttp:
    def __init__(self):
        pass

    async def fetch(self, session, url):
        async with session.get(url, ssl=False) as resp:
            return await resp.text()

    async def main(self):
        pattern = re.compile(r'\<title\>(?P<title>.*)\<\/title\>')
        urls = ('https://www.python.org/',
                'https://git-scm.com/',
                'https://www.jd.com/',
                'https://www.taobao.com/',
                'https://www.douban.com/')
        async with aiohttp.ClientSession() as session:
            for url in urls:
                html = await self.fetch(session, url)
                print(pattern.search(html).group('title'))

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())
        loop.close()

# 爬豆瓣的电影
class DouBanMovie():
    def __init__(self):
        # tag分类的url
        self.tag_url = 'https://movie.douban.com/j/search_tags?type=movie&source='
        # 获取电影的url
        self.movie_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=%s'
        # 分类的信息
        self.tags = []
        # 查询分页的深度
        self.page = 10
        conn = MongoClient('mongodb://127.0.0.1:27017')
        db = conn['douban1']
        # 操作表
        self.collection = db['spider']

    async def get_html_info(self):
        # 获取aiohttp的session实例，通过session去获取url的请求信息
        async with aiohttp.ClientSession() as session:
            async with session.get(self.tag_url) as response:
                # 使用await关键字，在获取网页的源码的时候，如果由于IO关系，
                # 数据一直没有响应，程序可以切换到其他地方去执行，等到有响应的时候，
                # 再切换回来执行
                tags = await self.parse(await response.text())
                self.tags =tags['tags']

            for tag in self.tags:
                for start_page in range(self.page):
                    async with session.get(self.movie_url % (tag, start_page*20)) as response:
                        data = await self.parse(await response.text())
                        for movie_info in data['subjects']:
                            await self.insert_into_db(movie_info)

    async def parse(self, response):
        # 将页面解析的api接口解析为python的字典对象
        tag_json = json.loads(response)
        return tag_json

    async def insert_into_db(self, data):
        # 插入到mongodb中
        self.collection.insert_one(data)

    def run(self):
        # 获取event_loop, 使用event_loop的run_until_complete去启动我们的任务
        loop = asyncio.get_event_loop()
        task = asyncio.wait([self.get_html_info()])
        loop.run_until_complete(task)




# 其他Http方法
# session.post('http://httpbin.org/post', data=b'data')
# session.put('http://httpbin.org/put', data=b'data')
# session.delete('http://httpbin.org/delete')
# session.head('http://httpbin.org/get')
# session.options('http://httpbin.org/get')
# session.patch('http://httpbin.org/patch', data=b'data')

# 自定义Headers
# payload = {'some': 'data'}
# headers = {'content-type': 'application/json'}
# await session.post(url, data=json.dumps(payload), headers=headers)

# 自定义Cookie
# cookies = {'cookies_are': 'working'}
# async with ClientSession(cookies=cookies) as session:
# 访问Cookie: session.cookie_jar

# 在URLs中传递参数
# 1. params = {'key1': 'value1', 'key2': 'value2'}
# 2. params = [('key', 'value1'), ('key', 'value2')]
# async with session.get('http://httpbin.org/get', params=params) as resp:
#     assert resp.url == 'http://httpbin.org/get?key2=value2&key1=value1'

# 发送数据
# payload = {'key1': 'value1', 'key2': 'value2'}
# async with session.post('http://httpbin.org/post', data=payload) as resp:
# async with session.post(url, data=json.dumps(payload)) as resp:
#     print(await resp.text())

# 发送文件(1)
# files = {'file': open('report.xls', 'rb')}
# await session.post(url, data=files)

# 发送数据(2)
# data = FormData()
# data.add_field('file',
#                open('report.xls', 'rb'),
#                filename='report.xls',
#                content_type='application/vnd.ms-excel')
# await session.post(url, data=data)

# 超时设置
# aync with session.get('https://github.com', timeout=60) as r:

# 代理支持
# async with aiohttp.ClientSession() as session:
#     async with session.get("http://python.org", proxy="http://some.proxy.com") as resp:
#         print(resp.status)

# async with aiohttp.ClientSession() as session:
#     proxy_auth = aiohttp.BasicAuth('user', 'pass')
#     async with session.get("http://python.org", proxy="http://some.proxy.com", proxy_auth=proxy_auth) as resp:
#         print(resp.status)
# session.get("http://python.org", proxy="http://user:pass@some.proxy.com")

# 返回的内容
# async with session.get('https://api.github.com/events') as resp:
#     print(await resp.text())
#     print(await resp.text(encoding='gbk'))
#     print(await resp.read())
#     print(await resp.json())

# 返回内容较大
# with open(filename, 'wb') as fd:
#     while True:
#         chunk = await resp.content.read(chunk_size)
#         if not chunk:
#             break
#         fd.write(chunk)

# 返回的其他变量
# async with session.get('http://httpbin.org/get') as resp:
#     print(resp.status)        # 状态码
#     print(resp.headers)       # Headers
#     print(resp.raw_headers)   # 原始Headers
#     print(resp.cookies)       # 返回的Cookie

# 访问历史History
# resp = await session.get('http://example.com/some/redirect/')
# resp: <ClientResponse(http://example.com/some/other/url/) [200]>
# resp.history: (<ClientResponse(http://example.com/some/redirect/) [301]>,)

# 释放返回的Response
# 1. async with session.get(url) as resp: pass
# 2. await resp.release()

# 连接器: Connectors
# conn = aiohttp.TCPConnector()
# session = aiohttp.ClientSession(connector=conn)

# 限制连接池大小:
# conn = aiohttp.TCPConnector(limit=30)
# conn = aiohttp.TCPConnector(limit=None)


# 异步IO例子：适配Python3.4，使用asyncio库
@asyncio.coroutine
def hello(index):                   # 通过装饰器asyncio.coroutine定义协程
    print('Hello world! index=%s, thread=%s' % (index, threading.currentThread()))
    yield from asyncio.sleep(1)     # 模拟IO任务
    print('Hello again! index=%s, thread=%s' % (index, threading.currentThread()))

# loop = asyncio.get_event_loop()     # 得到一个事件循环模型
# tasks = [hello(1), hello(2)]        # 初始化任务列表
# loop.run_until_complete(asyncio.wait(tasks))    # 执行任务
# loop.close()                        # 关闭事件循环列表


# 异步IO例子：适配Python3.5，使用async和await关键字
async def hello1(index):            # 通过关键字async定义协程
    print('Hello world! index=%s, thread=%s' % (index, threading.currentThread()))
    await asyncio.sleep(1)          # 模拟IO任务
    print('Hello again! index=%s, thread=%s' % (index, threading.currentThread()))

# loop = asyncio.get_event_loop()     # 得到一个事件循环模型
# tasks = [hello1(1), hello1(2)]      # 初始化任务列表
# loop.run_until_complete(asyncio.wait(tasks))    # 执行任务
# loop.close()                        # 关闭事件循环列表


# aiohttp 实例
async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(url, resp.status)
            print(url, await resp.text())

# loop = asyncio.get_event_loop()     # 得到一个事件循环模型
# tasks = [                           # 初始化任务列表
#     get("http://zhushou.360.cn/detail/index/soft_id/3283370"),
#     get("http://zhushou.360.cn/detail/index/soft_id/3264775"),
#     get("http://zhushou.360.cn/detail/index/soft_id/705490")
# ]
# loop.run_until_complete(asyncio.wait(tasks))    # 执行任务
# loop.close()                        # 关闭事件循环列表


# def my_test1():
#     while True:
#         print("test1......")
#         time.sleep(1)
#         yield
#
# def my_test2():
#     while True:
#         print("test2......")
#         time.sleep(1)
#         yield
#
# def main():
#     g1 = my_test1()
#     g2 = my_test2()
#     while True:
#         next(g1)
#         next(g2)

# 使用协程
# def my_test1():
#     for i in range(3):
#         print("test1......",i)
#         yield
#         time.sleep(1)
#
# def my_test2():
#     for i in range(3):
#         print("test2......",i)
#         yield
#         time.sleep(1)
#
# def main():
#     g1 = my_test1()
#     g2 = my_test2()
#     for i in range(3):
#         next(g1)
#         next(g2)
#     print("结束了")
# if __name__ == "__main__":
#     main()



# 使用greenlet
#
#
# def test1():
#     print('test1....01')
#     gr2.switch()
#     print('test1....02')
#     gr2.switch()
#
#
# def test2():
#     print('test2....01')
#     gr1.switch()
#     print('test2....02')
#
#
# # 1、将要执行的函数封装到greenlet对象中
# gr1 = greenlet.greenlet(test1)
# gr2 = greenlet.greenlet(test2)
# # 2、想先执行哪个函数就可以对象.swith()方法进行执行
# gr1.switch()

# 使用greenlet+协程
# - gr1=greenlet(目标函数)
# - fgr1.switch() 切换执行
# def my_test1():
#     for i in range(5):
#         print("test1......",i)
#         gr2.switch()
#         time.sleep(1)
#
# def my_test2():
#     for i in range(5):
#         print("test2......",i)
#         gr1.switch()
#
# if __name__=="__main__":
#     # 将要执行的函数封装到greenlet对象中
#     gr1 = greenlet.greenlet(my_test1)
#     gr2 = greenlet.greenlet(my_test2)
#     # 想先执行哪个函数就可以先用 对象.switch()方法进行执行
#     # gr1.switch()
#     gr1.switch()
#     print('程序结束了......')
#
# # gevent模块
# import gevent
# # 如果程序中没有耗时操作就顺序执行。
# def my_test1():
#     for i in range(5):
#         print('test1...', i)
#         time.sleep(1)
#         # gevent.sleep()，自带耗时函数
#         # gevent.sleep(1)  # 使用耗时模块可以自动操作
#
#
# def my_test2():
#     for i in range(5):
#         print('test2...', i)
#         # 自带耗时函数，当使用这个函数时，cpu会跳转到另一个就绪的程序，达到人工设置让其自动切换的功能
#         # 如果需要使用time.sleep()，修傲导入monkey，from gevent import monkey
#         #
#         gevent.sleep(1)
#
#
# if __name__ == '__main__':
#     # 可以用joinall函数一次生成多个
#     # gevent.joinall([gevent.spawn(my_test1),gevent.spawn(my_test2)])
#     # gevent.spawn的使用
#     g1 = gevent.spawn(my_test1)
#     g2 = gevent.spawn(my_test2)
#     g1.run()
#

#下面所有的但凡设计到的io操作,相当于打个标记
def eat(name):
    print('%s eat 1' % name)
    time.sleep(3)
    print('%s eat 2' % name)

def play(name):
    print('%s play 1' % name)
    time.sleep(4)
    print('%s play 2' % name)

#异步
g1=gevent.spawn(eat,'egon')
g2=gevent.spawn(play,'alex')
#在上面的任务执行之后,线程才死
time.sleep(5)

#主线程等着上面两个任务死了,在死  join()
#g1.join()
#g2.join()

#主线程等着上面两个任务死了,在死
gevent.joinall([g1,g2])

#图片下载器
def download_img(url,img_name):
    res = requests.get(url)
    with open('img/'+img_name,mode='wb') as f:
        f.write(res.content)

if __name__=="__main__":
    url = 'https://www.baidu.com'
    gevent.joinall({
        gevent.spawn(download_img,url,'panda1.png')
    })


    print("cpu count:", multiprocessing.cpu_count(), "\n")

    print("========== 直接执行IO密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    task_io(0)
    print("结束：", time.time() - time_0, "\n")

    print("========== 多线程执行IO密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    thread_list = [threading.Thread(target=task_io, args=(i,)) for i in range(5)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        if t.is_alive():
            t.join()
    print("结束：", time.time() - time_0, "\n")

    print("========== 多进程执行IO密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    process_list = [multiprocessing.Process(target=task_io, args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in process_list:
        p.start()
    for p in process_list:
        if p.is_alive():
            p.join()
    print("结束：", time.time() - time_0, "\n")

    print("========== 直接执行CPU密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    task_cpu(0)
    print("结束：", time.time() - time_0, "\n")

    print("========== 多线程执行CPU密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    thread_list = [threading.Thread(target=task_cpu, args=(i,)) for i in range(5)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        if t.is_alive():
            t.join()
    print("结束：", time.time() - time_0, "\n")

    print("========== 多进程执行cpu密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    process_list = [multiprocessing.Process(target=task_cpu, args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in process_list:
        p.start()
    for p in process_list:
        if p.is_alive():
            p.join()
    print("结束：", time.time() - time_0, "\n")

    exit()




    ta = Test_Aiohttp()
    ta.run()

    # dbm = DouBanMovie()
    # dbm.run()




    myprocess = My_Process()
    print("parent process is {}".format(os.getpid()))
    print(" ")
    p = Process(target=myprocess.run_proc,args=('test',))
    print("child process will start")
    # 进程只要start就会在开始运行了,所以p1-p4.start()时,系统中已经有四个并发的进程了
    # p.join()是在等p结束,p只要不结束主线程就会一直卡在原地
    p.start()
    p.join()
    print("child process will end")


    print("获取父进程：{}".format(os.getpid()))
    print(" ")
    # 定义一个进程池，允许4个进程并行
    p = Pool(4)
    # 依次启动4个进程
    for i in range(5):
        p.apply_async(myprocess.long_time_task,args=(i,))
    print('hehe')
    # 关闭进程池，不再接受新的进程
    # 当进程池close的时候并未关闭进程池，只是会把状态改为不可再插入元素的状态
    p.close()
    # 主进程阻塞等待子进程的退出
    p.join()
    print("over")



    mythread = My_Thread()
    print('非my_thread中thread {} is running......'.format(threading.current_thread().name))
    print(" ")
    t = threading.Thread(target=mythread.my_thread,name='my_thread_0709')
    t.start()
    t.join()
    print(" ")
    print('非my_thread中thread {} ended......'.format(threading.current_thread().name))