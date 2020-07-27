# -*- coding = utf-8 -*-
"""
@time:2020-07-09 14:48:59
@project:python_all_0511
@file:re_handler.py
@author:Jiang ChengLong
"""

import re

# re.match
line= "Cats are smarter than dogs"
matchObj = re.match(r'(.*) are (.*?) .*',line,re.M|re.I)
print(matchObj.groups())
print(matchObj.group())
print(matchObj.group(0))
print(matchObj.group(1))
print(matchObj.group(2))
# print(matchObj.group(3))

a  = re.match(r'^(\d+?)(0*)$','102300')
print(a.group())
print(a.group(1))
print(a.group(2))


# re.findall
match = re.findall("ab", "acbaacbab")
print(match)


# re.search
print(re.search('www','www.baidu.com'))
print(re.search('www','www.baidu.com').span())
# print(re.search('www','www.baidu.com').match)


