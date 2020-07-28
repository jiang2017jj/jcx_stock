#!/usr/bin/env python3
#-*- coding = utf-8 -*-

import os
import importlib
import sys
import time
import os.path
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
excel_path = os.path.join(os.getcwd(),'python_excel.xlsx')

importlib.reload(sys)
time1 = time.time()
# print("初始时间为：",time1)

text_path = r'words-words.pdf'

# text_path = r'photo-words.pdf'

# pdf文件处理：
# https://www.cnblogs.com/wj-1314/p/9429816.html
# https://www.jianshu.com/p/d078d8bcc9e8

def parse():
    '''解析PDF文本，并保存到TXT文件中'''
    fp = open(text_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(r'2.txt', 'a') as f:
                        results = x.get_text()
                        print(results)
                        f.write(results + "\n")


'''
假定有一个加密的 PDF 文件，你忘记了口令，但记得它是一个英语单词。尝试猜测遗忘的口令是很无聊的任务。
作为替代，你可以写一个程序，尝试用所有可能的英语单词来解密这个 PDF 文件，直到找到有效的口令。
这称为暴力口令攻击。从http://nostarch.com/automatestuff/下载文本文件 dictionary.txt。
这个字典文件包含 44000多个英语单词，每个单词占一行。利用第 8 章学过的文件读取技巧来读取这个文件，创建一个单词字符串的列表。
然后循环遍历这个列表中的每个单词，将它传递给 decrypt()方法，如果这个方法返回整数 0，口令就是错的，程序应该继续尝试下一个口令。
如果 decrypt()返回 1，程序就应该终止循环，打印出破解的口令。
你应该尝试每个单词的大小写形式（在我的笔记本上，遍历来自字典文件的所有 88000 个大小写单词，只要几分钟时间。这就是不应该使用简单英语单词作为口令的原因）。

暴力破解pdf：
https://blog.csdn.net/dongyu1703/article/details/82801047

暴力破解zip：
https://www.jianshu.com/p/2759264c9fe1

'''
import PyPDF2

file = open('dictionary.txt', 'r')

pdfReader = PyPDF2.PdfFileReader(open('encryptedmiutes.pdf', 'rb'))
dictionary = []
for line in file.readlines():
    dictionary.append(line.rstrip())
    dictionary.append(line.rstrip().lower())

for word in dictionary:
    number = pdfReader.decrypt(word)
    if number == 1:
        print(f"The password: {word}")
        break
file.close()



if __name__ == '__main__':
    parse()
    time2 = time.time()
    print("总共消耗时间为:", time2 - time1)
