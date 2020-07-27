# -*- coding = utf-8 -*-
"""
@time:2020-07-06 18:33:09
@project:apiauto2020
@file:testReportHandler.py
@author:Jiang ChengLong
"""
import os
import time
import json

'''
文本报告生成器
TODO:报告内容数据隔离，可以只记录报告格式和内容，不实际输出问题。例如，提供给邮件发送
'''

class ReportHandler():
    def __init__(self, reportPath='testResult/', reportName='report'):
        self.nowTime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(time.time()))
        if os.path.isdir(reportPath):
            self.reportPath = reportPath + reportName + '_' + str(self.nowTime) + '.txt'
        else:
            self.reportPath = reportPath

        self.fp = open(self.reportPath, 'w+')

    # 写入标题
    def reportToTitle(self, data):
        self.fp.writelines(data + '\r\n')

    # 写入时间
    def reportToDateTime(self):
        self.fp.writelines('时间:' + self.nowTime + '\r\n')

    # 写入描述信息
    def reportToDescription(self, data):
        self.fp.writelines(data + '\r\n')

    # 写入报告人
    def reportToAuthor(self, data):
        self.fp.writelines('报告人:' + data + '\r\n')

    # 写入一级标题
    def reportToLevel1(self, data):
        self.fp.writelines('=' * 30 + '\r\n')
        self.fp.writelines(data + '\r\n')

    # 写入二级标题和内容
    def reportToLevel2(self, info, content):
        self.fp.writelines('\t' + str(info) + ':' + str(content) + '\r\n')

    # 写入三级标题和内容
    def reportToLevel3(self, info, content):
        self.fp.writelines('\t' * 2 + str(info) + ':' + str(content) + '\r\n')

    # 写入空行
    def reportToBlankLine(self):
        self.fp.writelines('' + '\r\n')

    # 结束报告
    def endReport(self):
        self.fp.close()


# 题库专项测试测试报告输出
def genrateTikuReportResult(source, homeworkListAPI, checkSectionList, wrongSectionDicts, wrongHomeworkDict,
                            checkQuestionlist, wrongQuestionList):
    print('开始写报告...')
    report = ReportHandler(reportPath='/Users/autotest/Desktop/servertest/SusuanApiAutoTest-pyunit/src/testResult/',
                          reportName=str(source) + '-作业题目专项验证报告')
    report.reportToTitle(str(source) + '-作业题目专项验证报告')
    report.reportToDateTime()
    report.reportToDescription('验证范围：按照章节顺序检查数学日常作业章节题目是否数量无误；选择题题目数据是否正常可提交作答。')
    report.reportToAuthor('QA团队')

    # 分析章节扫描数据并生成报告
    report.reportToLevel1('【章节】扫描情况')
    report.reportToLevel2('扫描章节数', len(checkSectionList))
    wrongSectionTypeNum = 0
    wrongSectionNum = 0
    for wrongKey in wrongSectionDicts:
        wrongSectionTypeNum += 1
        report.reportToLevel3('问题类型' + str(wrongSectionTypeNum), wrongKey)
        report.reportToLevel3('错误章节列表' + str(wrongSectionTypeNum),
                              str(json.dumps(wrongSectionDicts[wrongKey], ensure_ascii=False)))
        report.reportToBlankLine()
        wrongSectionNum += len(wrongSectionDicts[wrongKey])
    if wrongSectionNum > 0:
        report.reportToLevel2('有误的章节数', wrongSectionNum)
    else:
        report.reportToLevel2('章节题目数量校验通过！', '')

    # 分析题目扫描数据并生成报告
    report.reportToLevel1('【题目】扫描情况')
    report.reportToLevel2('扫描题目数', len(checkQuestionlist))
    report.reportToLevel2('错误questionId', wrongQuestionList)

    # 分析作业扫描数据并生成报告
    report.reportToLevel1('【作业】扫描情况')
    report.reportToLevel2('扫描作业数', len(homeworkListAPI))
    report.reportToLevel2('错误作业详情', str(json.dumps(wrongHomeworkDict, ensure_ascii=False)))

    report.endReport()
    print('报告结束')

if __name__=="__main__":
    # 具体项目业务场景再完善
    pass