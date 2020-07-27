import functools
from random import randint
import time
import pymysql
import threading

"""
装饰器 - 装饰器中放置的通常都是横切关注（cross-concern）功能
所谓 横切关注功能 就是很多地方都会用到但跟正常业务又逻辑没有必然联系的功能
装饰器实际上是实现了设计模式中的 代理模式  - AOP（面向切面编程）
"""
# 不带参数的装饰器函数logging，自身不带参数，那么它就带func参数
def logging(func):
    # 为了保住func的愿名字
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        print("%s called" % func.__name__)
        result = func(*args, **kwargs)
        print("%s end" % func.__name__)
        return result
    return decorator


# 本身带参数的装饰器函数record_decorate，而且参数是另一个函数，高大上；一般参数是字符串之类的。
def record_decorate(output):
    def decorate(func):
        # 加wraps装饰器，主要是为了保住原函数的名字，更加专业
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            start = time.time()
            res_value = func(*args,**kwargs)
            output(func.__name__,time.time()-start)
            return res_value
        return wrapper
    return decorate


# 输出到控制台
def output_to_console(fname,duration):
    # 保留3位小数
    print('{}:{:.3f}秒'.format(fname,duration))

# 输出到文件
def output_to_file(fname, duration):
    with open('log.txt','a',) as file_stream:
        file_stream.write('%s: %.3f秒\n' % (fname, duration))

# 输出到数据库进行存储
def output_to_db(fname,duration):
    conn = pymysql.connect(host='localhost', port=3306,
                      database='test', charset='utf8',
                      user='root', password='123456',
                      autocommit=True)
    try:
        with conn.cursor() as cursor:
            cursor.execute(('insert into tb_record values (default, %s, %s)',(fname, '%.3f' % duration)))
    except Exception as e:
        return e
    finally:
        conn.close()



# 使用不带参数的装饰器方法logging
@logging
def test_logging_01(a, b):
    print("in function test01, a=%s, b=%s" % (a, b))
    return 1


# 使用不带参数的装饰器方法logging
@logging
def test_logging_02(a, b, c=1):
    print("in function test02, a=%s, b=%s, c=%s" % (a, b, c))
    return 1

# 使用带参数的装饰器函数record_decorate
@record_decorate(output_to_console)
def test_record_decorate_01(min_number, max_number):
    print("11111")
    time.sleep(randint(min_number, max_number))
    print("22222")


# 同时使用多个装饰器方法
@logging
@record_decorate(output_to_console)
def test_both_01(a, b, c):
    print("in function test05, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 在类的成员方法中使用装饰器方法record_decorate
class ATest(object):
    @record_decorate(output_to_console)
    def test(self, a, b):
        print("in function test of ATest, a=%s, b=%s" % (a, b))
        time.sleep(2)
        print("end......")
        return 1


# 上面都是装饰器方法，装饰器类也是一样可用的
# 不带参数的装饰器类
class My_Decorator_1():
    def __init__(self,func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("%s called" % self.func.__name__)
        result = self.func(*args, **kwargs)
        print("%s end" % self.func.__name__)
        return result


# 带参数的装饰器类
class My_Decorator_2():
    def __init__(self,*types,**kwtypes):
        self.types = types
        self.kwtypes = kwtypes

    def __call__(self, func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            result1 = [isinstance(_param, _type) for _param, _type in zip(args, self.types)]
            assert all(result1), "params_chack: invalid parameters"
            # 为什么会报错呢？
            result2 = [isinstance(kwargs[_param], self.kwtypes[_param]) for _param in kwargs if _param in self.kwtypes.keys()]
            assert all(result2), "params_chack: invalid parameters"
            return func(*args, **kwargs)
        return _inner


# 使用不带参数的装饰器类
@My_Decorator_1
def test_Decorator_01(a, b, c):
    print("in function test06, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 使用带参数的装饰器类
@My_Decorator_2(int, str, (list, tuple))
def test_Decorator_02(a, b, c):
    print("in function test06, a=%s, b=%s, c=%s" % (a, b, c))
    return 1



# 理论结合实际的应用，装饰器实例: 函数缓存
def funccache(func):
    cache = {}

    @functools.wraps(func)
    def _inner(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return _inner

# 使用装饰器
@funccache
def test_cache_01(a, b, c):
    # 其他复杂或耗时计算
    return a + b + c



"""
装饰类的装饰器函数 -实现 单例模式 - 一个类只能创建出唯一的对象
上下文语法：__enter__ / __exit__
"""
# 定义类的装饰器函数，这会是不带参数的类,cls代表将要被修饰的类。
# 还有一种是装饰器带参数的，同函数，后续自己完成；
def singleton(cls):
    """单例装饰器"""
    instances = {}
    lock = threading.Lock()
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            # with lock:
            #     if cls not in instances:
            #         instances[cls] = cls(*args, **kwargs)
            with lock:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class President():

    def __init__(self, name, country):
        self.name = name
        self.country = country

    def __str__(self):
        return f'{self.country}: {self.name}'



if __name__ == '__main__':
    # at = ATest()
    for i in range(3):
        pass
        # test_logging_01(1,2)
        # test_logging_02(1,2,3)
        # test_record_decorate_01(1,2)
        # test_both_01(1,2,3)
        # at.test(1,2)
        # test_Decorator_01(1,2,3)
        # test_Decorator_02(1,2,3)
        # test_cache_01(1,2,3)
        # 取消掉装饰器
        # test_record_decorate_01.__wrapped__(3,5)
    print(President.__name__)
    p1 = President('特朗普', '美国')
    p2 = President('奥巴马', '美国')
    print(p1 == p2)
    print(p1)
    print(p2)