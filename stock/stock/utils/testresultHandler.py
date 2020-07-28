# -*- coding: utf-8 -*-
# !/usr/bin/env pytho

import time, re
import sys
from random import choice

from handlers.logHandler import Jcl_Logger

nowTime = time.strftime("%Y%m%d %H%M%S", time.localtime(time.time()))

'''
接口特殊返回码过滤规则
如果不在规则范围内，认为异常
如果在规则范围内，但规则码不包含实际Code码，认为异常
'''

# log记录：Jcl_Logger('jcllogger').getlog().debug("调用getFileNew方法异常:{}".format(e))

def filterSpecialCode(requestPath, realResultCode):
    filterFlag = True

    commonRuleList = [10002, 20003]

    normalRuleDict = {'/user/auth/register-verify-code': [20029],
                      '/hurdle/section/get-second-page': [20018],
                      '/arena/challenge/search': [32003],
                      '/html5/user/send-sms': [20029],
                      '/user/auth/register-mobile-exists': [20002],
                      '/exercise/multiple-steps/level-list': [40010],
                      '/classpk/class-pk/start-pk': [20040],
                      '/html5/user/check-user': [20021],
                      '/hurdle/box/open-box': [20102],
                      '/exercise/english/level-list': [40010],
                      '/user/auth/forget-check-verify-code': [20021],
                      '/admin-student/student/info-by-mobile': [53002],
                      '/adapt/ability/get-recommend-question': [20085],
                      '/classpk/class-pk/start-through': [20040],
                      '/arena/section/pk-questions': [20014],
                      '/exercise/chinese/level-list': [40010],
                      '/recreation/through/unlock-checkpoin': [20205],
                      '/user/auth/forget-verify-code': [20029],
                      '/phrase/guess/get-reward': [30101],
                      '/exercise/exercise/level-list': [40010]
                      }
    # 如果实际返回码不在通用特殊码中，则认为是一个需要继续检查的返回码
    if realResultCode not in commonRuleList:
        # 如果实际返回码不在可接受的范围中，则认为是一个错误的返回
        if requestPath in normalRuleDict:
            if realResultCode not in normalRuleDict[requestPath]:
                filterFlag = False
        else:
            filterFlag = False
    return filterFlag


''''
get参数由字符串转为dict
参数示例：getStr="classId=1008280&deviceModel=iPhone"
'''
def changeGetStrToDict(getStr):
    getDict = {}
    getList = getStr.split('&')
    for oneGetInfo in getList:
        try:
            getDict[oneGetInfo.split('=')[0]] = oneGetInfo.split('=')[1]
        except:
            continue
    return getDict


'''
awk '{print $13}' studentAccessGet.log|awk -F '?' '{print $1}'|sort|uniq -c|sort -nr -k1|head -20
解析原nginx请求日志中access_log内容为可执行请求http的dict内容,示例access_log单行内容：
Sep  8 01:59:59 10-9-163-54 nginx: 2018-09-08T01:59:59+08:00 - 0.021 - 200 - GET /user/auth/register-verify-code?source=androidRCStudent&v
ersion=3935&appVersion=3.9.35&platform=Android&appName=RCStudent&channel=tencent&deviceId=863
064010003129&umid=null&deviceVersion=4.4.2&deviceType=HUAWEIMLA-AL10&transaction=getRegisterCode&mobile=15802682
617&sendCnt=0 HTTP/1.1 - - - [44] - 10.215.52.44:90       01 - 0.021 - 117.81.244.192
'''
def analyzeOriginLogToHttpSource(coreURIs, reqHost):
    httpSourceList = []
    for line in coreURIs:
        httpDict = {}
        httpDict['method'] = 'GET'
        httpDict['host'] = reqHost

        # 获取请求uri
        try:
            uriStartIndex = line.index('/')
            uriEndIndex = line.index('?')
        except:
            # get请求没有参数，说明无效请求，不进行回放
            continue
        httpDict['path'] = line[uriStartIndex:uriEndIndex]

        # 获取请求get参数
        httpDict['paramDict'] = {}
        getParamEndIndex = line.index('HTTP/1.1') - 1
        getStr = line[uriEndIndex + 1:getParamEndIndex]
        httpDict['paramDict'] = changeGetStrToDict(getStr)

        httpSourceList.append(httpDict)
    return httpSourceList


'''
发送http请求并返回必要结果
'''
def requestHttp(httpSourceList, replayTimeSleep):
    httpResultList = []
    errorStatus = 0
    notHttp200ResultList = []
    notCode99999ResultList = []
    errorResult = {'notHttp200': notHttp200ResultList,
                   'notCode99999': notCode99999ResultList}
    requestCount = 0

    for oneRequest in httpSourceList:
        httpResult = ['httpCode', 'path', 'detail', 'url']

        '''发送http请求'''
        reqHandler = requestHandler.REQHandler()
        uri = oneRequest['path']
        reqHost = oneRequest['host']
        try:
            # 写日志error
            Jcl_Logger('jcllogger').getlog().debug("正在请求:{}".format(uri))

            if oneRequest['method'] == 'GET':
                ret = reqHandler.getRequest(reqHost=reqHost, uri=uri, specialDict=oneRequest['paramDict'])
            elif oneRequest['method'] == 'POST':
                ret = reqHandler.postRequest(reqHost=reqHost, uri=uri, specialDict=oneRequest['paramDict'])
            del reqHandler
        except:
            httpResult[0] = -1

        '''组装必要结果'''
        if 'errorCode' in ret:
            httpResult[0] = int(ret['errorCode'])
        else:
            httpResult[0] = 200
        try:
            httpResult[1] = oneRequest['path']
            httpResult[2] = ret[2]
        except:
            httpResult[1] = oneRequest['path']
            httpResult[2] = ret['errorReason']
        httpResult[3] = oneRequest['paramDict']

        httpResultList.append(httpResult)
        requestCount = requestCount + 1

        '''记录异常的请求'''
        if httpResult[0] != 200:
            errorStatus = 1
            notHttp200ResultList.append(httpResult)
        else:
            if ret[2]['code'] != 99999 and ret[2]['code'] != '99999':
                # 检查是否命中了特殊规则，如果也没有命中特殊规则，则确认该接口有异常
                if filterSpecialCode(oneRequest['path'], ret[2]['code']) == False:
                    errorStatus = 1
                    notCode99999ResultList.append(httpResult)
            errorResult = {'notHttp200': notHttp200ResultList,
                           'notCode99999': notCode99999ResultList}

        time.sleep(replayTimeSleep)

    print('共请求' + str(requestCount) + '个接口完毕!')
    return httpResultList, errorStatus, errorResult


''''
钉钉报警
'''
def sendDingDing(message):
    reqHost = 'oapi.dingtalk.com'
    uri = '/robot/send?access_token=9117278720e350dac0da0ce23eb22ae48cdd78b4b3081bcba67c9e3833f2860f'
    postContent = {
        "msgtype": "text",
        "text": {
            "content": "请相关同学尽快查看并解决"
        },
        "at": {"isAtAll": True},

    }
    postContent2 = {
        "msgtype": "link",
        "link": {
            "title": "线上定时任务执行失败b",
            "text": "失败任务yii aaa/bb",
            "picUrl": "https://app.knowbox.cn/ss/images/pcbanner.png",
            "messageUrl": "http://117.50.7.111:8080/jenkins/view/crontab/job/test_crontab2/4479/console"
        },
        "at": {
            "atMobiles": [],
            "isAtAll": True
        }
    }
    postContent3 = {
        "actionCard": {
            "title": "线上定时任务执行失败",
            "text": "#### 线上定时任务执行失败 \n\n adfasdfasdfasdfasdf信息",
            "hideAvatar": "0",
            "btnOrientation": "0",
            "btns": [
                {
                    "title": "查看详情",
                    "actionURL": "http://117.50.7.111:8080/jenkins/view/crontab/job/test_crontab2/4479/console/"
                }
            ],
            "at": {
                "atMobiles": [],
                "isAtAll": True
            }
        },
        "msgtype": "actionCard"
    }
    #     {
    #         "actionCard":
    #         {
    #             "title": "线上定时任务执行失败",
    #             "text": "asdfadfasdf(点击查看详情:http://117.50.7.111:8080/jenkins/view/crontab/job/test_crontab2/4479/console)",
    #             "hideAvatar": "0",
    #             "btnOrientation": "0",
    #             "picURL":"https://app.knowbox.cn/ss/images/pcbanner.png"
    #         },
    #         "msgtype": "actionCard"
    #     }

    reqHandler = requestHandler.REQHandler()
    reqHandler.PROTOCAL = 'https'
    reqHandler.postRequest(reqHost=reqHost, uri=uri, specialDict=postContent)
    del reqHandler


''''
根据log文件进行回访请求并记录
'''
def replayLogByURIList(coreURIs, reqHost, oneReplayToSleep=0.1):
    '''解析access_log文件'''
    httpSourceList = analyzeOriginLogToHttpSource(coreURIs, reqHost)
    '''回放请求并记录结果'''
    httpResultAll, errorStatus, errorResult = requestHttp(httpSourceList, oneReplayToSleep)

    '''分析结果并输出'''
    if errorStatus == 0:
        print
        '本次api重放无异常！'
        # 写日志error
        aLog = logHandler.LogHandle(logPath)
        aLog.dataToLogInfo('本次api重放无异常！')
        del aLog
    else:
        print('本次api重放异常结果：',errorResult)

        # 写日志error
        Jcl_Logger('jcllogger').getlog().debug("本次api重放异常结果:{}".format(str(errorResult)))

        # 发送钉钉报警
        sendDingDing(errorResult)

    print('-' * 30)

    print('本次回放所有api接口及返回结果：',httpResultAll)

    # 写日志error
    Jcl_Logger('jcllogger').getlog().debug(str(errorResult) + '-' * 30+'本次回放所有api接口及返回结果:'+str(httpResultAll))


''''
获取list中元素出现位置
'''
def find_repeat(source, elmt):
    elmt_index = []
    s_index = 0;
    e_index = len(source)
    while (s_index < e_index):
        try:
            temp = source.index(elmt, s_index, e_index)
            elmt_index.append(temp)
            s_index = temp + 1
        except ValueError:
            break
    return elmt_index


''''
根据log进行接口uri分类，挑选核心接口
如果isFillterOneCoreURI=1，则每个接口随机挑选fillterCounterEachURI个加入回放列表
如果isFillterOneCoreURI=0，则返回全部接口
'''
def selectCoreLog(accessLogPath, isFillterOneCoreURI=1, fillterCounterEachURI=1, rePatternStr=None):
    # 加载文件获取全部的uri行
    f = open(accessLogPath, 'r')
    allLog = f.readlines()
    f.close()
    allLogRealURI = [row for row in allLog if '?' in row]
    allURIs = [row[row.index('/'):row.index('?')] for row in allLogRealURI]

    # 获取所有的uri种类
    allUniqURIs = list(set(allURIs))
    if isFillterOneCoreURI == 1:
        coreURIs = []
        for oneURI in allUniqURIs[:]:
            # 如果设置了正则，按照正则再过滤一次接口
            if rePatternStr is not None:
                pattern = re.compile(rePatternStr)  # 查找数字
                reResult = pattern.findall(oneURI)
                # 不匹配正则，跳过当前uri
                if len(reResult) == 0:
                    continue

            # 获取uri出现次数
            findIndexs = find_repeat(allURIs, oneURI)
            if fillterCounterEachURI == 1:
                randomIndex = choice(findIndexs)
                coreURIs.append(allLogRealURI[randomIndex:randomIndex + 1][0])
            else:
                if findIndexs < fillterCounterEachURI:
                    addCount = findIndexs
                else:
                    addCount = fillterCounterEachURI
                for i in range(0, addCount):
                    randomIndex = choice(findIndexs)
                    coreURIs.append(allLogRealURI[randomIndex:randomIndex + 1][0])

        return allUniqURIs, coreURIs
    else:
        return allUniqURIs, allLogRealURI


if __name__ == '__main__':
    sendDingDing("crontab执行失败:")
    exit(0)
    if len(sys.argv) < 4:
        print('请输入完整参数执行！')

        print("示例命令 python replayAccessLog_start.py <access_log_path> <domainHost> <secondToSleep> <retPattern可选>",sys.exit())


    print('开始：' + time.strftime("%Y年%m月%d日_%H:%M:%S", time.localtime(time.time())))

    '''定义回放日志路径和请求环境'''
    accessLogPath = str(sys.argv[1])  # '/Users/autotest/Desktop/logs/studentAccessGet.log'
    reqHost = str(sys.argv[2])  # 'preshark.knowbox.cn:8041'
    oneReplayToSleep = float(sys.argv[3])  # 0.5
    logPath = accessLogPath[:accessLogPath.rindex('/')] + '/log_' + nowTime + '.log'
    if len(sys.argv) == 5:
        rePatternStr = sys.argv[4]
        print('按照正则表达式匹配筛选接口，正则：' + str(rePatternStr))

    else:
        rePatternStr = None

    '''解析日志获取核心接口'''

    allUniqURIs, coreURIs = selectCoreLog(accessLogPath, isFillterOneCoreURI=1, fillterCounterEachURI=2,
                                          rePatternStr=rePatternStr)

    print('全部接口：', allUniqURIs)

    print('全部接口种类数量：', len(allUniqURIs))

    print('回放接口：', coreURIs)

    print('回放数量：', len(coreURIs))

    # 写日志error
    aLog = logHandler.LogHandle(logPath)
    aLog.dataToLogInfo('回放接口：' + str(coreURIs))
    aLog.dataToLogInfo('回放数量：' + str(len(coreURIs)))
    del aLog

    print('过滤接口完毕：' + time.strftime("%Y年%m月%d日_%H:%M:%S", time.localtime(time.time())))

    '''回放日志'''
    replayLogByURIList(coreURIs, reqHost, oneReplayToSleep=oneReplayToSleep)

    print('结束：' + time.strftime("%Y年%m月%d日_%H:%M:%S", time.localtime(time.time())))

