import json
import os
import re
import codecs
from lxml import etree
from bs4 import BeautifulSoup
from py._xmlgen import unicode

# 找到测试结果存储的目录testresults
htmlresult_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testresults')


class HtmlHandler:

    def __init__(self):
        self.html_Path = os.path.join(htmlresult_path, 'htmls')

    def get_html_data(self,html_name):
        try:
            with codecs.open(os.path.join(self.html_Path,html_name), "r", "utf-8") as f:
                content = f.read()

            # 获取html树，通过xpath获取指定内容
            tree = etree.HTML(content)
            node = tree.xpath("//div[@class='content']")[0]
            node.text.encoding('gbk')

            # 通过正则表达式 获取<tr></tr>之间指定的内容
            res_tr = r'<tr>(.*?)</tr>'
            m_tr = re.findall(res_tr,content,re.S|re.M)
            for line in m_tr:
                print(line)
                #获取表格第一列th 属性
                res_th = r'<th>(.*?)</th>'
                m_th = re.findall(res_th,line,re.S|re.M)
                for mm in m_th:
                    print(unicode(mm,'utf-8')) #unicode防止乱
                    # #获取表格第二列td 属性值
                res_td = r'<td>(.*?)</td>'
                m_td = re.findall(res_td,line,re.S|re.M)
                for nn in m_td:
                    print(unicode(nn,'utf-8'))
        except Exception as e:
            print(e)

    def get_html_data_by_soup(self):
        lists = []
        with codecs.open(self.html_Path, "r", "utf-8") as f:
            content = f.read()
        Soup = BeautifulSoup(content, 'lxml')
        print(Soup)
        titles = Soup.select('td')
        print(titles)
        for title in titles:
            lists.append(title.text)
            print(lists)

    def delete_html_file(self):
        # 数据获取后，将生成的测试报告全部删除，防止干扰下次测试
        for root, dirs, files in os.walk(self.html_Path):
            for name in files:
                os.remove(os.path.join(root, name))



if "__main__" ==__name__:
    # 根据具体业务场景继续完善
    hh = HtmlHandler()
    print(hh.get_html_tree())
