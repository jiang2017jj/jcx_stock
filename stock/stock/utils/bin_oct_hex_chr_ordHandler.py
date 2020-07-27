c = input("请输入一个字符：")
# 必须有int
a = int(input("请输入一个ASCII码："))

print("字符对应的ascii码为：",ord(c))
print("ascii对应的字符为：",chr(a))

num = int(input("请输入一个数字："))

print("转换成二进制为：",bin(num))
print("转换成八进制为：",oct(num))
print("转换成十六进制为：",hex(num))
