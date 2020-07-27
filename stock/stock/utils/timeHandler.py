#!/usr/bin/env python3
#-*- coding = utf-8 -*-


import calendar
import datetime
import time


# 日历相关
def display_month(yyyy,mm):
    if mm<1 or mm>12:
        return u'输入的月份不存在'
    else:
        print('{}-{}的月历展示：'.format(yyyy,mm))
        print(calendar.month(yyyy,mm))


def display_monthrange(yyyy,mm):
    if mm<1 or mm>12:
        return u'输入的月份不存在'
    else:
        # 结果是一个元组，第一个代表是星期几，0-6，0代表周一；第二个是本月有多少天
        print('{}-{}：'.format(yyyy,mm))
        print(calendar.monthrange(yyyy,mm))


def display_calendar_year(yyyy):
    if mm < 1 or mm > 12:
        return u'输入的月份不存在'
    else:
        # 打印2019年，3个月一行，横向看每天相差w个字符，每月相差c个字符，l为每星期占用的行数,每行长度为 21*W+18+2*C
        # print('{}-{}：'.format(yyyy, mm))
        # 打印年历，3个月一行，横向看每天相差w个字符，每月之间相差c个字符，l是每星期占用的行数，每行的总长度：21w+18+2c
        print(calendar.calendar(yyyy,w=2,l=1,c=6))

def display_calendar_month(yyyy,mm):
    if mm < 1 or mm > 12:
        return u'输入的月份不存在'
    else:
        # 如果是打印某个月的，则用month，同时有个月份参数，没有c参数,而且方法名是month
        # print('{}-{}：'.format(yyyy, mm))
        # 打印年历，3个月一行，横向看每天相差w个字符，每月之间相差c个字符，l是每星期占用的行数，每行的总长度：21w+18+2c
        print(calendar.month(yyyy,mm,w=2,l=2))


# datetime相关
def get_yesterday():
    # 获取今天的日期
    today = datetime.date.today()
    print(today)
    # 获取一天的时间间隔，输出为 1 day，0：00：00
    oneday = datetime.timedelta(days=1)
    print(oneday)
    # 今天减去一天，就是昨天
    yesterday = today-oneday
    return yesterday

def get_days_ago(n):
    # 得到的格式是---标准格式，同时秒后面带小数点
    ndaysago = datetime.datetime.now()-datetime.timedelta(days=n)
    print(ndaysago)
    # 时间转换为时间戳
    timestamp = int(time.mktime(ndaysago.timetuple()))
    print(timestamp)
    # 转换格式，为秒后面为小数点
    change_into_other_style = ndaysago.strftime("%Y/%m/%d %H:%M:%S")
    print(change_into_other_style)

def stamp_into_time(time_stamp,n):
    # 将时间转换成标准时间格式用utcfromtimestamp
    date_arr = datetime.datetime.utcfromtimestamp(time_stamp)
    ndaysago = date_arr - datetime.timedelta(days=n)
    print(ndaysago)

def time_stampintotime(my_stamp):
    # 拿到的是时间戳
    now = time.time()
    print(now)
    print(my_stamp)
    # 拿到得失time.struct_time格式：
    # time.struct_time(tm_year=2020, tm_mon=1, tm_mday=6, tm_hour=17, tm_min=42, tm_sec=38, tm_wday=0, tm_yday=6, tm_isdst=0)
    time_arr = time.localtime(now)
    time_arr2 = time.localtime(my_stamp)
    print(time_arr)
    print(time_arr2)
    # 从struct_time转换为其他格式的时间，用strftime
    otherstyletime = time.strftime("%Y-%m-%d %H:%M:%S",time_arr)
    otherstyletime2 = time.strftime("%Y-%m-%d %H:%M:%S", time_arr2)
    print(otherstyletime)
    print(otherstyletime2)

def datetime_stampintotime(my_stamp):
    #拿到的是正常的时间格式，但是秒后面有小数点
    now = datetime.datetime.now()
    print(now)
    print(my_stamp)
    # datetime中针对时间戳还需要将时间戳处理一下,已经是标准时间格式了
    datetime_arr = datetime.datetime.utcfromtimestamp(my_stamp)
    print(datetime_arr)
    # 通过XX.strftime()函数将XX转换为标准时间格式
    otherstyletime = now.strftime("%Y-%m-%d %H:%M:%S")
    otherstyletime2 = datetime_arr.strftime("%Y-%m-%d %H:%M:%S")
    print(otherstyletime)
    print(otherstyletime2)

# print(get_yesterday())
# get_days_ago(3)
# stamp_into_time(157283888884,3)
# time_stampintotime(1557502800)
datetime_stampintotime(1557502800)



# time相关
# 将字符串时间转换成structime格式，然后再转换成时间戳
def str_time_to_str(str_time):
    # striptime()返回的是time.struct_time(tm_year=2019, tm_mon=12, tm_mday=12, tm_hour=12, tm_min=12, tm_sec=12, tm_wday=3, tm_yday=346, tm_isdst=-1)
    # striptime()参数必须是字符串时间+时间格式化，不能省略
    my_struct_time = time.strptime(str_time,'%Y-%m-%d %H:%M:%S')
    #利用mktime将struct_time转换成时间戳
    # mktime（）接收struct_time对象作为参数，返回用秒数来表示时间的浮点数。也可以接收完整的9位元组元素。
    # t = (2016, 2, 17, 17, 3, 38, 1, 48, 0)
    # secs = time.mktime( t )
    my_time_stamp = time.mktime(my_struct_time)
    print(my_time_stamp)


# 将时间展示格式从一种转换为另一种,例如从2019/11/11 转换成2019-11-11
def change_time_format_by_strftime(str_time):
    # 套路都是先转换为struct_time，strptime第一个参数是时间，第二个参数是格式
    my_struct_time = time.strptime(str_time,'%Y/%m/%d %H:%M:%S')
    my_new_format_time = time.strftime('%Y-%m-%d %H:%M:%S',my_struct_time)
    print(my_new_format_time)

# 时间戳转换成为具体的时间格式
def timestamp_to_format(timestamp1):
    struct1 = time.localtime(timestamp1)
    print(struct1)
    # strftime方法的第一个参数是我们自定义的格式
    format = time.strftime("%Y-%m-%d %H:%M:%S", struct1)
    print(format)

# 时间戳转固定的时间字符串，Fri Jul 17 14:47:29 2020
def timestamp_to_str(stamp):
    a = time.ctime(stamp)
    print(a)

# 接受一个structtime格式，转换成特定的时间字符串,Fri Jul 17 14:57:52 2020
def struct_to_str():
    time1 = time.localtime(time.time())
    print(time1)
    a = time.asctime(time1)
    print(a)


# utc时间也是同理，接受一个structtime格式，转换成特定的时间字符串,Fri Jul 17 6:57:52 2020,时间少8个小时
def utc_struct_to_str():
    time1 = time.gmtime(time.time())
    print(time1)
    a = time.asctime(time1)
    print(a)



# 获取datetime.datetime类型的本地时间，正常的时间格式，非时间戳
def fmt_time_1():
    a = datetime.datetime.now(tz=None)
    print('方法里面：',a)
    # 将datetime.datetime类型的时间转换为字符串格式的时间
    str_time = a.strftime("%Y-%m-%d, %H:%M:%S, %w")
    print(str_time)

# 这样就能输出
a = datetime.datetime.now(tz=None)
print('直接输出',a)
# 将datetime.datetime类型的时间转换为字符串格式的时间
print('直接输出',a.strftime("%Y-%m-%d, %H:%M:%S, %w"))
# 将datetime.datetime类型的时间转换为时间戳
print('直接输出',a.timestamp())
# 将时间戳转换成date.date类型的时间
print('直接输出',datetime.datetime.fromtimestamp(time.time()))
# datetime类型转struct_time类型
print('直接输出',a.timetuple())


def fmt_time_2():
    a = datetime.datetime.utcnow()
    print('方法里面：',a)

# 这样就能输出
b = datetime.datetime.utcnow()
print('直接输出',b)
# 将datetime.datetime类型的时间转换为字符串格式的时间
print('直接输出',b.strftime("%Y-%m-%d, %H:%M:%S, %w"))
# 将datetime.datetime类型转换为时间戳
print('直接输出',b.timestamp())
# 将时间戳转换成date.date类型的时间
print('直接输出',datetime.datetime.utcfromtimestamp(time.time()))
# datetime类型转struct_time类型
print('直接输出',b.timetuple())


# 字符串 转 datetime.datetime格式,%w前面必须有空格！
a_datetime = datetime.datetime.strptime("2016-11-15, 15:32:12, 2", "%Y-%m-%d, %H:%M:%S, %w")
print('直接输出',a_datetime)




if __name__ == "__main__":
    # time.strptime()是核心，因为它将格式的时间转换成struct_time格式
    # 然后mktime将struct_time格式转换成 本地时间戳
    # 或者strftime将struct_time格式转换成其他格式的时间

    # time.gmtime()也是核心之一，返回的是utc时间的structime格式
    # utc_time = time.gmtime(),拿到utc时间的struct_time格式
    # 然后calendar.timegm(utc_time) 将struct_time类型的utc时间转换成 本地时间戳

    # time.localtime()也是核心，是将时间戳转换成structime格式
    # 然后通过strftime将strutime格式转成想要的格式的时间

    # time.time()返回的结果是时间戳，计算时间间隔的时候可以取不同时间的时间戳进行减法运算。

    # str_time_to_str('2019-12-12 12:12:12')
    # change_time_format_by_strftime('2019/12/12 12:12:12')
    # timestamp_to_format(1577851932)
    # a = time.gmtime()
    # print(calendar.timegm(a))

    # timestamp_to_str(1594968449)

    # struct_to_str()

    # utc_struct_to_str()

    struct_time = time.strptime("2016-11-15, 15:32:12, 2", "%Y-%m-%d, %H:%M:%S, %w")  # 字符串转struct_time类型
    print(struct_time)


    yyyy = int(input('请输入年份，如1950：'))
    mm = int(input('请输入月份，如04：'))
    display_month(yyyy,mm)
    display_monthrange(yyyy,mm)
    display_calendar_year(yyyy)
    display_calendar_month(yyyy,mm)



    fmt_time_1()
    fmt_time_2()


