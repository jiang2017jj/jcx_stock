import unicodedata

"""
https://www.cnblogs.com/jebeljebel/p/4006433.html
-- 数字的表达式操作符
    yield x                                      # 生成器函数发送协议
    lambda args: expression                      # 生成匿名函数
    x if y else z                                # 三元选择表达式
    x and y, x or y, not x                       # 逻辑与、逻辑或、逻辑非
    x in y, x not in y                           # 成员对象测试
    x is y, x is not y                           # 对象实体测试
    x<y, x<=y, x>y, x>=y, x==y, x!=y             # 大小比较，集合子集或超集值相等性操作符
    1 < a < 3                                    # Python中允许连续比较
    x|y, x&y, x^y                                # 位或、位与、位异或
    x<<y, x>>y                                   # 位操作：x左移、右移y位
    +, -, *, /, //, %, **                        # 真除法、floor除法：返回不大于真除法结果的整数值、取余、幂运算
    -x, +x, ~x                                   # 一元减法、识别、按位求补（取反）
    x[i], x[i:j:k]                               # 索引、分片
    int(3.14), float(3)                          # 强制类型转换
"""

def is_number1(num):
    try:
        # isdigit()判断num中是否都是数字
        if num.isdigit():
            return u"全部都是数字"
    except ValueError:
        pass

    try:
        # 将一个合法的数值字符串转化成数字值
        if unicodedata.digit(num):
            return u"把一个合法的数值字符串转换成数字值"
    except (TypeError, ValueError):
        pass

    try:
        # 将数值转换成浮点数
        float(num)
        return u'是一个整数或者浮点数'
    except ValueError:
        pass

    try:
        # isnumeric（）判断num是不是一个包含中文数字，阿拉伯数字的组合
        # 例如 三4五 会被识别出来
        if num.isnumeric():
            return u'是一个包含中文数字，阿拉伯数字的组合'
    except (TypeError, ValueError):
        pass

    try: # 将一个合法的数字字符串转换成浮点数返回
        unicodedata.numeric(num)
        return u'把一个表示数字的字符串转换成浮点数返回，任意表示数值的字符都可以'
    except (TypeError,ValueError):
        pass
    # try:
    #     a = unicodedata.decimal(num)
    #     return u'只能拿全部是数字的字符'+ a
    # except (TypeError,ValueError):
    #     pass

    return u'输入的内容包含数字和非数字内容，或者全部都是非数字'

if __name__=="__main__":

    num1 = unicodedata.digit("2")
    print(num1)

    num2 = unicodedata.numeric("Ⅷ")
    print(num2)

    num3 = unicodedata.numeric("八")
    print(num3)

    for i in range(20):
        a = input("请输入内容，判断是否是数字：")
        print(is_number1(a))


