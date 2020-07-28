import os

"""
大前提
python中所有的迭代环境都会先尝试__iter__方法，再尝试__getitem__方法，只有在对象不支持 迭代协议 时，才会尝试索引；

在python中实现了__iter__方法的对象是可迭代的，实现了next()方法的对象是迭代器
也就是说可以被next 函数调用并不断返回下一个值的对象称为迭代器
也等价于实际上要想让一个迭代器工作，至少要实现__iter__方法和next()方法
实际用起来，如果一个类想被用于for ... in循环，类似list或tuple那样：
首先就必须实现一个__iter__()方法，该方法返回一个迭代对象
然后Python的for循环就会不断调用该迭代对象的next()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环
当你或是一个循环机制(例如 for 语句)需要下一个项时, 调用迭代器的 next() 方法就可以获得它
条目全部取出后, 会引发一个 StopIteration 异常
这并不表示错误发生, 只是告诉外部调用者, 迭代完成

根本上说, 迭代器就是有一个 next() 方法的对象, 也就是：含有__next__()函数的对象都是一个迭代器，而不是通过索引来计数.
"""

# 将任何一个类打造成一个迭代器，需要实现两个方法__iter__和__next__，
class JclNumbers():
    # 在迭代器的类中，__iter__和__next__是必须的，__init__不是必须的
    def __init__(self):
        self.a = 0
        self.b = 1
    #定义一个__iter__方法，表示这个类是一个迭代器，只在迭代开始的时候运行一次，返回的是对象本身
    def __iter__(self):
        # __iter__只执行一次，所以可以用来赋值；也可以在__init__中赋值
        # self.a = 0
        # self.b = 1
        return self

    # 这个迭代器对象实现了__next__()方法，编写要输出的值的逻辑,同时for循环调用的时候，会默认调用__next__方法；
    def __next__(self):
        # 计算下一个值
        self.a,self.b = self.b,self.a+self.b
        if self.a >= 100:
            # 并通过StopIteration异常标识迭代的完成，防止出现无限循环的情况
            raise StopIteration
        return self.a

# 实例化这个类
jclnumbers = JclNumbers()

# 实例化的对象，已经可以使用for循环输出
# for in做了两件事：1。获得了一个可迭代器，即调用了__iter__方法；2。循环过程调用了__next__方法
for x in jclnumbers:
    print(x)

# 对象也可以作为iter()的参数
jclnumbers_iter = iter(jclnumbers)
# 用for循环输出
# for in做了两件事：1。获得了一个可迭代器，即调用了__iter__方法；2。循环过程调用了__next__方法
for x in jclnumbers_iter:
    print(x)

# 此外对一个对象调用iter()方法，即可将这个对象变为迭代器，例如list1 = [1,2,3,4,5]
# 即如果你传递一个参数给 iter()，它会检查你传递的是不是一个序列, 如果是, 那么很简单,根据索引从 0 一直迭代到序列结束.
list1 = [1,2,3,4,5]
list_iter = iter(list1)
# 用for循环输出
# for in做了两件事：1。获得了一个可迭代器，即调用了__iter__方法；2。循环过程调用了__next__方法
for x in list_iter:
    print(x)


"""
迭代器是一个对象，生成器是一个函数,两者对于python来说非常重要
迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束
迭代器只能往前不会后退
可以使用isinstance()判断一个对象是否是迭代器对象(iterator)
迭代器有两个基本的方法：iter()和next()
新增内建函数：reversed(),enumerate(),any(),all(),以及有itertools模块；range(n)生成的也是迭代器对象
还引用了3个新的内建字典方法来定义迭代：iterkeys(),itervalues(),iteritems()
需要放在try...except中；
"""

# next()还有一种用法
it = iter([1,2,3,4])
while True:
    try:
        x=next(it)
        print(x)
    except StopIteration:
        break



# 使用生成器来生成斐波那契数列，生成器是一个函数，有yield，返回值是一个 迭代器；简单的说，生成器就是迭代器
def fib(n):
    num1,num2 = 0,1
    while num2<=n:
        yield num2
        num1,num2 = num2,num1+num2

if __name__=="__main__":
    # 调用fib（）不会有任何输出，生成器处于空闲状态，此时num1,num2 = num2,num1+num2并未执行
    a = fib(1000)
    # 将生成器包含在list（）中，list会根据传进来的参数生成一个列表，所以调用了next方法，此时打印b这个列表就会输出
    b = list(a)
    print(b)