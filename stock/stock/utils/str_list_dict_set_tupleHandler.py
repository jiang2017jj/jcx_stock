# _*_ coding: utf-8 _*_

from fn import _
from operator import add
from functools import partial, reduce


# 各种生成式

# 列表生成式
a_list = [item**2 for item in range(5)]
print(a_list)


# 字典生成式
a_dict = {"%d_key" % item: item**2 for item in range(5)}
print(a_dict)


# 生成器生成式，也可以叫迭代器生成式
a_generator = (item**2 for item in range(5))
print(a_generator)
print(next(a_generator))
print(next(a_generator))


# iter函数和next函数，iter函数生成迭代器
a_list_generator = iter(a_list)
print(next(a_list_generator))
print(next(a_list_generator))
print(type(a_list), type(a_list_generator))


# lambda表达式
a_func = lambda x, y: x**y
print(a_func(2, 3))


# map函数
print(map(abs, range(-4, 5)))
print(list(map(abs, range(-4, 5))))
print(list(map(lambda x: x**2, range(5))))
# 相同位置的一个是x一个是y，而且以短的为准；map() 会根据提供的函数对指定序列做映射。
# 第一个参数 function 以参数序列中的每一个元素调用 function 函数，python2返回包含每次 function 函数返回值的新列表，
# python3返回的是一个迭代器，需要用list（）转换成列表。
print(list(map(lambda x, y: x**y, range(1, 5), range(1, 5))))


# reduce函数
# 在 Python3 中，reduce() 函数已经被从全局名字空间里移除了，它现在被放置在 functools 模块里，
# 如果想要使用它，则需要通过引入 functools 模块来调用 reduce() 函数：
# reduce() 函数会对参数序列中元素进行累积。
# 函数将一个数据集合（链表，元组等）中的所有数据进行下列操作：用传给 reduce 中的函数 function（必须有两个参数）
# 先对集合中的第 1、2 个元素进行操作，得到的结果再与第3个数据用 function 函数运算，最后得到一个结果，
# 第3个参数要注意，这是初始值，累加的和的初始值。
print(reduce(lambda x, y: x+y, range(10)))
print(reduce(lambda x, y: x+y, range(10), 100))
# 列表相加，最后会成为一个大列表
print(reduce(lambda x, y: x+y, [[1, 2], [3, 4]], [0]))
# operator.add函数与reduce方法类似
print(reduce(lambda x, y: x+y, range(10)))
print(reduce(add, range(10)))


# filter函数，filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。
# 该接收两个参数，第一个为函数，作用是判断真假的，专门为了过滤，
# 第二个为序列，序列的每个元素作为参数传递给函数进行判断，然后返回 True 或 False，
# 最后将返回 True 的元素放到新列表中。python3会返回迭代器，需要用list（）方法转换成列表。
print(filter(None, range(-4, 5)))
print(list(filter(None, range(-4, 5))))
print(list(filter(lambda x: x > 0, range(-4, 5))))


# all、any函数
# all() 函数用于判断给定的可迭代参数 iterable 中的所有元素是否都为 TRUE，如果是返回 True，否则返回 False。
# 元素除了是 0、空、None、False 外都算 True。
print(all([0, 1, 2]))

# any() 函数用于判断给定的可迭代参数 iterable 是否全部为 False，则返回 False，如果有一个为 True，则返回 True。
# 元素除了是 0、空、FALSE 外都算 TRUE。
print(any([0, 1, 2]))


# enumerate函数,index的值是赠送的
for index, item in enumerate(range(6,11)):
    print("%d: %d" % (index, item))


# zip函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
# 如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表，
# zip在python3中返回是一个对象。
for a, b in zip([1, 2, 3], ["a", "b", "c"]):
    print(a, b)

# zip返回的对象直接用dict（）加持，能直接生成字典，前面介绍字典的生成方式的时候也有讲解
a_dict = dict(zip([1, 2, 3], ["a", "b", "c"]))
print(a_dict)


# partial函数
# 这种写法和下面的partial写法会得到同样的结果
print(int("10010", base=2))
# 第一个参数是int等类型，第二个参数是base
int_base_2 = partial(int, base=2)
print(int_base_2("10010"))


# fn的使用
from fn import _
add_func_1 = (_ + 2)
print(add_func_1(1))
add_func_2 = (_ + _ * _)
print(add_func_2(1, 2, 3))


# 一行代码启动一个Web服务
# python -m SimpleHTTPServer 8080
# python3 -m http.server 8080


# 一行代码实现变量值互换
a, b = 1, 2; a, b = b, a


# 一行代码解决FizzBuzz问题: 打印数字1到100, 3的倍数打印“Fizz”来替换这个数, 5的倍数打印“Buzz”, 既是3又是5的倍数的打印“FizzBuzz”
print(' '.join(["fizz"[x % 3 * 4:]+"buzz"[x % 5 * 4:] or str(x) for x in range(1, 101)]))


# 一行代码输出特定字符"Love"拼成的心形
print('\n'.join([''.join([('Love'[(x-y) % len('Love')] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))


# 一行代码输出Mandelbrot图像: Mandelbrot图像中的每个位置都对应于公式N=x+y*i中的一个复数
print('\n'.join([''.join(['*'if abs((lambda a: lambda z, c, n: a(a, z, c, n))(lambda s, z, c, n: z if n == 0 else s(s, z*z+c, c, n-1))(0, 0.02*x+0.05j*y, 40)) < 2 else ' ' for x in range(-80, 20)]) for y in range(-20, 20)]))


# 一行代码打印九九乘法表
print('\n'.join([' '.join(['%s*%s=%-2s' % (y, x, x*y) for y in range(1, x+1)]) for x in range(1, 10)]))


# 一行代码计算出1-100之间的素数(两个版本)
print(' '.join([str(item) for item in filter(lambda x: not [x % i for i in range(2, x) if x % i == 0], range(2, 101))]))
print(' '.join([str(item) for item in filter(lambda x: all(map(lambda p: x % p != 0, range(2, x))), range(2, 101))]))


# 一行代码输出斐波那契数列
print([x[0] for x in [(a[i][0], a.append([a[i][1], a[i][0]+a[i][1]])) for a in ([[1, 1]], ) for i in range(30)]])


# 一行代码实现快排算法
qsort = lambda arr: len(arr) > 1 and qsort(list(filter(lambda x: x <= arr[0], arr[1:]))) + arr[0:1] + qsort(list(filter(lambda x: x > arr[0], arr[1:]))) or arr


# 一行代码解决八皇后问题
[__import__('sys').stdout.write('\n'.join('.' * i + 'Q' + '.' * (8-i-1) for i in vec) + "\n========\n") for vec in __import__('itertools').permutations(range(8)) if 8 == len(set(vec[i]+i for i in range(8))) == len(set(vec[i]-i for i in range(8)))]


# 一行代码实现数组的flatten功能: 将多维数组转化为一维
flatten = lambda x: [y for l in x for y in flatten(l)] if isinstance(x, list) else [x]


# 一行代码实现list, 有点类似与上个功能的反功能
array = lambda x: [x[i:i+3] for i in range(0, len(x), 3)]


# 一行代码实现求解2的1000次方的各位数之和
print(sum(map(int, str(2**1000))))


# 最后推荐一篇文章: [Python One-liner Games](http://arunrocks.com/python-one-liner-games/)
exit()


my_dict = {
    "a":5,
    "b":6,
    "c":7,
    "d":8
}

jcl_dict = {
    "e":5,
    "f":6,
    "g":7,
    "h":9
}

def dict_to_str(my_dict):
    str_list = ["%s\t%s" % (key, my_dict[key]) for key in my_dict]
    return "\n".join(str_list)


def contains_key(dict,key):
    # 判断字典中是否包含某个key，一句代码搞定
    return key in dict

if __name__=="__main__":
    my_dict_1 = {'a': 'jcl', 'b': 'jcx'}
    print(dict_to_str(my_dict_1))
    print(my_dict['a'])
    print(my_dict.pop('b'))
    print(my_dict.pop('b','没有这个key了'))
    new_dict = {key:value for key,value in my_dict.items() if key!='d' }
    print("新字典：",new_dict)
    # update执行完毕后没有任何输出，new_dict1这个其实并不是字典，是个None，必须打印my_dict才能看到。。。。。。
    new_dict1 = my_dict.update(jcl_dict)
    print(new_dict1)
    print(my_dict)
    # print("删除前的字典",my_dict)
    #
    # del my_dict['a']
    #
    # print("删除后的字典：",my_dict)
    #
    # removed_item1 = my_dict.pop("b")
    #
    # print("删除的元素的值：",removed_item1)
    #
    # print("删除后的字典：",my_dict)
    #
    # removed_item2 = my_dict.pop("e","没有该key")
    #
    # print(removed_item2)
    #
    # # 需要用到my_dict.items(),删除了key=d的元素，从而生成了新的字典
    # new_dict = {key:value for key,value in my_dict.items() if key!='d' }
    # print("新字典：",new_dict)


line = ['a','b','c','d','e']

print(line[-1])

# 去除了这一行文本的最后一个字符（换行符）后剩下的部分
print(line[:-1])

newline = line[::-1]
print(newline)

line = 'abcde'

print(line[:-1])


str = "www.baidu.com"

# 判断所有字符都是数字或者字母
print(str.isalnum())

# 判断所有字符都是字母
print(str.isalpha())

# 判断所有字符都是数字
print(str.isdigit())

#判断所有字符都是小写字母
print(str.islower())

#判断所有字符都是大写字母
print(str.isupper())

# 判断所有单词都是首字母大写，像标题
print(str.istitle())

# 判断所有字符是否是空白字符，\t,\n ,\r
print(str.isspace())

# 将字符改变
str1 = 'www.baidu.com'

# 将字符传中的字符都变成大写
print(str1.upper())

# 将字符传中的字符都变成小写
print(str1.lower())

# 字符串所有单词的首字母都大写
print(str1.title())

# 将字符串中第一个字母大写
print(str1.capitalize())

# 判断字符串是否包含子串,-1代表不存在，其余的值代表存在；
# 返回的是索引值在字符串中的起始位置。如果不包含索引值，返回-1。
print('abcde'.find('abc'))



def exec_code():
    LOC = """
def factorial(num):
    fact = 1
    for i in range(1,num+1):
        fact = fact * i
    return fact
print(factorial(5))    
    """
    # exec（）方法，直接将字符串翻译成可执行的代码进行执行。。。。。。
    exec(LOC)

exec_code()



# 序列赋值必须一一对应，下面会
# x,y,z = 'abcd'
# 正确的如下
# x,y,z = 'abc'
# 序列解包,这样也可以，前后取一个，剩下的都给中间的那个,以列表形式给y
x,*y,z = 'abcd'

# 列表-增强赋值，数字则不一样，通过运行结果可见，
# python中列表变量的“赋值b=a”并没有新建一个列表，而是将b指向了与a的同一个列表。b与a共同指向一个列表“实例”。
a=b=[1,2]
a+=[3,4]

# 数字，是新建了两个变量，分别赋值为1，互相不影响
c=d=1
c+=1
print(x)
print(y)
print(z)
print(a)
print(b)
print(c)
print(d)



def some_is_instance(l):
    if isinstance(l,list):
        print(l,"是列表")
    else:
        print(l,"请重新检查输入")

some_is_instance([1,2,3])
some_is_instance((1,2,3))