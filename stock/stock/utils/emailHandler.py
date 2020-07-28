#!/usr/bin/env python
# coding=utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import datetime
from email.header import Header
from os import path
from config import sender, receivers, sender_login, sender_login_pwd
from logHandler import Jcl_Logger

#邮件类
class EmailHandler(object):
    def __init__(self):
        Jcl_Logger('jcllogger').getlog().debug("开始实例化EmailHandler类")
        # 获取年月日
        self.year = datetime.datetime.now().year
        self.month = datetime.datetime.now().month
        self.day = datetime.datetime.now().day
        self.test_result_path = os.path.join(os.path.dirname(path.dirname(__file__)), 'testresults')
        Jcl_Logger('jcllogger').getlog().debug("实例化EmailHandler类成功")

    # 获取最新生成的测试结果,这个方法有问题，需要重新写0723;
    def getFileNew(self):
        Jcl_Logger('jcllogger').getlog().debug("开始调用getFileNew方法")
        try:
            # 查找测试报告文件夹test_result_path，找到最新生成的测试报告，lists是所有结果组成的列表
            self.test_result_lists = os.listdir(self.test_result_path)
            # sort按key的关键字进行升序排序，lambda的入参fn为lists列表的元素，获取文件的最后修改时间，所以最终以文件时间从小到大排序
            self.test_result_lists.sort(key=lambda fn: os.path.getmtime(os.path.join(self.test_result_lists,fn)))
            file_new = self.test_result_lists[-1]
            # 增加日志
            return file_new
        except Exception as e:
            Jcl_Logger('jcllogger').getlog().debug("调用getFileNew方法异常:{}".format(e))


    #发送纯文本邮件MIMEText()，qq邮箱则需要先配置邮箱的设置,设置-账户-开启两个服务，具体可搜索查询
    def send_html_mail(self):
        try:
            mail_body = ""
            # 调用方法获取最新的那条测试报告
            file_new = self.getFileNew()
            if file_new:
                with open(file_new,'rb',encoding='utf-8') as f:
                    mail_body = f.read()
            msg = MIMEText(mail_body, 'html', 'utf-8')
            msg['Subject'] = Header('接口测试报告', 'utf-8')
            msg['From'] = sender
            msg['To'] = receivers
            #发送机制
            smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
            smtp.login(sender_login,sender_login_pwd)
            smtp.sendmail(sender,receivers,msg.as_string())
            smtp.quit()
        except Exception as e:
            Jcl_Logger('jcllogger').getlog().debug("调用send_html_mail方法异常:{}".format(e))
            return None

    #发送带附件的测试报告邮件MIMEMultipart()
    def send_att_mail(self,date=None):
        # 调用方法获取最新的那条测试报告
        file_new = self.getFileNew()
        if file_new:
            with open(file_new, 'rb', encoding='utf-8') as f:
                mail_body = f.read()

        # 构建邮件正文
        body = MIMEText(mail_body, 'html', 'utf-8')
        msg=MIMEMultipart()
        msg['Subject'] = Header('接口测试报告（不带附件）', 'utf-8')
        msg['From'] = sender
        msg['To'] = receivers
        msg.attach(body)

        # 构建邮件附件
        # # MIMEBase表示附件的对象
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        # filename是显示附件名字
        att["Content-Disposition"] = 'attachment; filename="test_report.html"'
        msg.attach(att)

        # 发送邮件
        try:
            # 发送机制
            smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
            smtp.login(sender_login,sender_login_pwd)
            smtp.sendmail(sender, receivers, msg.as_string())
            smtp.quit()
        except Exception as e:
            Jcl_Logger('jcllogger').getlog().debug("调用ssend_att_mail方法异常:{}".format(e))
            return None

    # 计算接口执行成功失败率，后续完善
    def send_main(self,pass_list,fail_list,no_run_list):
        pass_num = len(pass_list)
        fail_num = len(fail_list)
        no_run_num = len(no_run_list)
        count_num = pass_num + fail_num + no_run_num
        #成功率、失败率
        '''
        用%对字符串进行格式化
        %d 格式化整数
        %f 格式化小数；想保留两位小数，需要在f前面加上条件：%.2f；用%%来表示一个%
        如果你不太确定应该用什么，%s永远起作用，它会把任何数据类型转换为字符串 
       '''
        try:
            pass_result = "%.2f%%" % (pass_num/count_num*100)
            fail_result = "%.2f%%" % (fail_num/count_num*100)
            no_run_result = "%.2f%%" % (no_run_num/count_num*100)
            # user_list = ['xxx@qq.com','xxx@qq.com']
            user_list = ['xxx@qq.com']
            sub = "接口自动化测试报告"
            content = "接口自动化测试结果:\n通过个数%s个，失败个数%s个，未执行个数%s个：通过率为%s，失败率为%s，未执行率为%s\n日志见附件" % (pass_num,fail_num,no_run_num,pass_result,fail_result,no_run_result)
            self.send_mail(user_list,sub,content)
        except Exception as e:
            Jcl_Logger('jcllogger').getlog().debug("调用send_main方法异常:{}".format(e))




if __name__=='__main__':
    eh = EmailHandler()
    eh.send_html_mail()
    # eh.send_att_mail()

    # test_dir = "D:\\APIinterfacetest\\apiauto\\test_case"
    # test_report = "D:\\APIinterfacetest\\apiauto\\report"
    # discover = unittest.defaultTestLoader.discover(test_dir,pattern='test*.py')
    # now = time.strftime("%Y-%m-%d_%H-%M-%S-",time.localtime())
    # #定义报告存放路径
    # filename = test_report+"\\"+now+"resutl.html"
    # fp = open(filename,"wb")
    # #定义测试报告
    # runner = HTMLTestRunner(stream=fp,title="订单中心测试接口",description="测试用例执行情况")
    # #运行测试
    # runner.run(discover)
    # #关闭报告文件写入磁盘
    # fp.close()
    # #发送邮件
    # new_report = new_report(test_report)
    # send_email(new_report)

