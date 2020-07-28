#!/usr/bin/env python3
#-*- coding = utf-8 -*-


"""
pyhton排序算法：
快速排序：
https://www.runoob.com/python3/python-quicksort.html
https://blog.csdn.net/qq_17753903/article/details/82765619
插入排序(比较常用插入排序只需要赋值一次)：
https://www.cnblogs.com/yeni/p/11162337.html
选择排序（和冒泡排序类似，但是每轮比较只需要交换一次，比较牛）：
https://www.cnblogs.com/xxtalhr/p/10787340.html
冒泡排序：
https://blog.csdn.net/qq_33356563/article/details/83628819
二分查找（针对有序序列进行某个元素的查找）：
https://blog.csdn.net/wang_8101/article/details/85227955

"""


# 反转数组,将长度为n的数组的前d个元素反转，然后放到数组尾部
class Reverse_List:
    def __init__(self,arr):
        self.arr = arr

    def reverse_arr(self,start,end):
        while (start<end):
            tmp = self.arr[start]
            self.arr[start] = self.arr[end]
            self.arr[end] = tmp
            start = start + 1
            end = end - 1

    def left_rotate(self,d):
        n = len(self.arr)
        self.reverse_arr(0,d-1)
        self.reverse_arr(d, n-1)
        self.reverse_arr(0, n-1)

    def print_arr(self):
        for i in range(0,len(self.arr)):
            print(self.arr[i],end=' ')


# 将数组的前d个元素先反转，然后放到数组的尾部
# https://www.runoob.com/python3/python3-array-rotation.html

# 将一个元素放到数组末尾,n为数组的长度
def my_reverse_one(lis,n):
    temp = lis[0]
    for i in range(0,n-1):
        lis[i]=lis[i+1]
    lis[n-1]= temp

#然后将前d个元素都这样操作，就实现了两个目的：元素翻转+放到末尾,哪里实现元素反转了？扯淡
def my_reverse_d1(lis,d,n):
    for i in range(d):
        my_reverse_one(lis,n)
    return lis

# lis = [1,2,3,4,5]
# a = my_reverse_d1(lis,2,5)
# print(a)


# 交换首尾位置
def my_reverse(arr,start,end):
    while(start<end):
        temp = arr[start]
        arr[start] = arr[end]
        arr[end] = temp
        start = start+1
        end = end-1

# 这是啥。。。。
def my_reverse_d2(arr,d):
    n = len(arr)
    my_reverse(arr,0,d-1)
    my_reverse(arr,d,n-1)
    my_reverse(arr,0,n-1)

def printArray(arr):
    for i in range(0,len(arr)):
        print(arr[i],end=' ')

arr = [1,3,5,7]
my_reverse_d2(arr,2)
printArray(arr)



# 给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
# 功能实现，但是效率较低
def reverse_force_1(x: int) -> int:
    if -10 < x < 10:
        return x
    str_x = str(x)
    if str_x[0] != "-":
        str_x = str_x[::-1]
        x = int(str_x)
    else:
        str_x = str_x[:0:-1]
        x = int(str_x)
        x = -x
    return x if -2147483648 < x < 2147483647 else 0

# 效率也不高
class Solution:
    def reverse(self, x: int) -> int:
        flag = 1
        if x < 0:
            flag = -1
            x = -x
        num_list = []

        while x:
            num_list.append(x % 10)
            x = x // 10
        num_sum = 0

        num_len = len(num_list)
        for i, item in enumerate(num_list):
            num_sum += item * 10 ** (num_len - i - 1)

        num_sum = flag * num_sum
        if (num_sum < - 2 ** 31) or (num_sum > 2 ** 31 - 1):
            return 0
        else:
            return num_sum


# 上面的方法执行效率太低，优化一下，一次构建反转整数的一位数字，这样做可以预先检查向原整数附加另一位数字是否会导致溢出，
# 反转整数类似于反转字符串,不断的弹出x的最后一位数字，驾到res的后面，最后res与x相反
def reverse_better(x: int) -> int:
    y, res = abs(x), 0
    # 则其数值范围为 [−2^31,  2^31 − 1]
    boundry = (1 << 31) - 1 if x > 0 else 1 << 31
    print(boundry)
    while y != 0:
        res = res * 10 + y % 10
        if res > boundry:
            return 0
        y //= 10
    return res if x > 0 else -res


# sorted(dict),与sort（）区别，sort（）只是针对list的，sorted（）是针对可迭代对象的
#按照字典的key进行排序
def dict_sort_by_key(dict):
    # i是字典对应的key,按照key进行排序
    for i in sorted(dict):
        print(i,dict[i],end=' ')
        print()

#按照字典的value进行排序
def dict_sort_by_value(dict):
    for i in sorted(dict.items(),key=lambda kv:(kv[1],kv[0]),reverse=False):
        print(i)

#按照字典的某个key进行排序，一般是针对列表了，列表中的元素是字典，字典中又包含多个键值对
def dict_sort_by_some_key(dict,some_key):
    for i in sorted(dict,key=lambda i:i[some_key]):
        print(i)

#先按照某个key升序排序，然后再按照另一个key升序排序，一般是针对列表了，列表中的元素是字典，字典中又包含多个键值对，需要能进行排序
def dict_sort_by_many_keys_1(dict,key1,key2):
    for i in sorted(dict,key=lambda i:(i[key1],i[key2])):
        print(i)

# 先按照某个key降序排序，然后再按照另一个key升序排序，一般是针对列表了，列表中的元素是字典，字典中又包含多个键值对
# 需要能够支持倒序排序，添加 - 这种倒序排序，一般是int
def dict_sort_by_many_keys_2(dict,key1,key2):
    for i in sorted(dict,key=lambda i:(-i[key1],i[key2])):
        print(i)

#按照单个某个key降序，直接加参数reverse即可
def dict_sort_by_reverse_para(dict,some_key):
    for i in sorted(dict,key=lambda i:i[some_key],reverse=True):
        print(i)



# 就是不断的找基准值，然后把比他小的放在左侧，把比他大的值放在右侧，递归到最后就完整排序了
def jcl_sort_1(L):
    # 如果列表只有一个元素或者没有元素，则直接返回
    if len(L) <= 1:
        return L
    # 否则返回一个列表，为列表表达式方式
    return jcl_sort_1([lt for lt in L[1:] if lt < L[0]]) + L[0:1]+ jcl_sort_1([ge for ge in L[1:] if ge >= L[0]])





# 最后一个参数-1必须带
for i in range(5,0,-1):
    print(i)

# 不带最后一个参数，不会输出
for i in range(5,1):
    print(i)




if __name__=="__main__":

    jcl_dict_1 = {
        5: "a",
        2: "b",
        3: "c"
    }

    jcl_dict_2 = [
        {'name': 'alice', 'score': 38},
        {'name': 'bob', 'score': 18},
        {'name': 'darl', 'score': 28},
        {'name': 'christ', 'score': 28}
          ]

    jcl_dict_3 = [
        {"name": "taobao", "age": 100},
        {"name": "zhihu", "age": 10},
        {"name": "google", "age": 50},
        {"name": "baidu", "age": 50},
    ]

    # dict_sort_by_key(jcl_dict_1)
    # dict_sort_by_value(jcl_dict_1)
    # 先按照得分倒序排列，然后同分的按照名字升序排列
    # print(sorted(jcl_dict_2, key=lambda x: (-x['score'], x['name'])))
    #按照age进行排序
    # dict_sort_by_some_key(jcl_dict_3,'age')
    # 先按照age升序，同名的再按照名字升序
    # dict_sort_by_many_keys_1(jcl_dict_3,'age','name')
    # 先按照age降序，同名的再按照名字升序
    dict_sort_by_many_keys_2(jcl_dict_3,'age','name')
    # dict_sort_by_reverse_para(jcl_dict_3,'age')



    iList = [3,14,2,12,9,33,99,35]
    print (jcl_sort_1(iList))



    print(reverse_force_1(123))
    print(reverse_better(123))
    print(reverse_better(-123))




    arr = [1,2,3,4,5,6,7]
    rl = Reverse_List(arr)
    rl.left_rotate(2)
    rl.print_arr()

