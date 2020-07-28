import decimal
from fractions import Fraction

# 定义小数精度位数
decimal.getcontext().prec = 2

#处理小数
def my_decimal(x,y):
    result = decimal.Decimal(x)+decimal.Decimal(y)
    return result

#处理分数
def my_fraction(x,y):
    a = Fraction(x,y)
    print(a)
    b = Fraction(0.25)
    print(b)
    return a,b

# 有一分数序列：2/1，3/2，5/3，8/5，13/8，21/13...求出这个数列的前20项之和。
# 能不能算出来是个分数呢，小数就不准确了，Fraction函数解决了这个问题。
def count_sum(n):
    # sum = Fraction(0,1)
    sum = 0
    i = 1
    a = 2
    b=1
    while i <= n:
        sum = sum + Fraction(a,b)
        print(sum)
        a,b = a+b,a
        i+=1
    return sum



if __name__=="__main__":
    print(my_decimal(0.01,0.02))
    # print(my_fraction(4,6))
    # print(count_sum(20))