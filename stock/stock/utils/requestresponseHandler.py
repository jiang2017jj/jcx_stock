import ssl
import urllib.request
import json
from config import PROTOCAL, HTTP_TIMEOUT
from handlers.logHandler import Jcl_Logger


# 日志需要后续慢慢改下：Jcl_Logger('jcllogger').getlog().debug("请求报错:{}，请求地址:{},报错信息:{}"）
class REQHandler():

    def __init__(self):
        pass

    def __getOne(self,reqHost,reqUri,getDataDict):
        uri = reqUri
        url = PROTOCAL+'://'+reqHost+uri
        requestPath = url+"?"
        for key in getDataDict:
            requestPath+=key+'='+str(getDataDict[key])+'&'
        #最后要去掉最后一个&
        requestPath=requestPath[:-1]

        response = None
        try:
            # 忽略SSL证书，解决Charles开启状态代码运行报错,https://blog.csdn.net/u013630017/article/details/51921144
            headers = { 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }
            response = urllib.request.urlopen(requestPath,timeout=HTTP_TIMEOUT,context=ssl._create_unverified_context())
        except urllib.request.URLError as e:
            errorCode = "-1"
            errorReson = ""
            if hasattr(e,"code"):
                errorCode = str(e.code)
            if hasattr(e,"reson"):
                errorReson = str(e.reason)
                Jcl_Logger('jcllogger').getlog().debug("请求报错:{}，请求地址:{},报错信息:{}".format(str(errorCode),str(requestPath),e.read()))
                return {'errorCode': errorCode, 'errorReason': errorReson, 'errorMsg': e.read()}
        finally:
            if response:
                # print '请求：',requestPath
                resultData = json.load(response, encoding='utf-8')
                getDataDict = json.dumps(getDataDict, ensure_ascii=False)
                response.close()
                # 写日志
                Jcl_Logger('jcllogger').getlog().debug('[{}][{}]get请求地址url:{}\n\t,返回结果:{}'.format(str(PROTOCAL),str(
                    response.code),requestPath,str(json.dumps(resultData, ensure_ascii=False))))

                if resultData is not None:
                    return (requestPath, getDataDict, resultData)
                else:
                    return {'errorCode': '-1', 'errorReason': 'resultData is None!'}


    def __postOne(self, reqHost, reqUri, postDataDict, getDataDict=None):
        uri = reqUri
        url = PROTOCAL + '://' + reqHost + uri
        requestPath = url
        response = None
        if getDataDict is not None:
            requestPath += '?'
            for key in getDataDict:
                requestPath += key + '=' + str(getDataDict[key]) + '&'
            requestPath = requestPath[:-1]

        try:
            requestUrl = urllib.request.Request(requestPath)
            # 忽略SSL证书，解决Charles开启状态代码运行报错
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            openUrl = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(), urllib.request.HTTPSHandler(context=ctx))
            requestUrl.add_header('Content-Type', 'application/json')
            requestUrl.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
            response = openUrl.open(requestUrl, json.dumps(postDataDict), timeout=self.HTTP_TIMEOUT)
        except urllib.request.URLError as e:
            errorCode = '-1'
            errorReson = ''
            if hasattr(e, 'code'):
                errorCode = str(e.code)
            if hasattr(e, 'reason'):
                errorReson = str(e.reason)
                # 写日志error
            Jcl_Logger('jcllogger').getlog().debug('[' + str(self.PROTOCAL) + '][' + str(errorCode) + ']请求地址url：' + requestPath + '\n\t提交post参数：' + str(
                    json.dumps(postDataDict, ensure_ascii=False)) + '\n\t返回结果详情请看服务器日志。')
            Jcl_Logger('jcllogger').getlog().debug('请求报错了。[' + str(errorCode) + ']请求地址：' + str(requestPath) + '提交post参数' + str(
                json.dumps(postDataDict, ensure_ascii=False)))
            Jcl_Logger('jcllogger').getlog().debug('报错信息：' + e.read())
            return {'errorCode': errorCode, 'errorReason': errorReson}
        finally:
            if response:
                resultData = json.load(response, encoding='utf-8')
                postDataDict = json.dumps(postDataDict, ensure_ascii=False)
                response.close()
                # 写日志
                Jcl_Logger('jcllogger').getlog().debug('[' + str(self.PROTOCAL) + '][' + str(
                    response.code) + ']post请求地址url：' + requestPath + '\n\t提交post参数：' + str(
                    postDataDict) + '\n\t返回结果：' + str(json.dumps(resultData, ensure_ascii=False)))

                if resultData is not None:
                    return (requestPath, postDataDict, resultData)
                else:
                    return {'errorCode': '-1', 'errorReason': 'resultData is None!'}

    def getRequest(self, reqHost, uri, **args):
        getDataDict = {}
        specialDict = None
        argDict = args
        for argKey in argDict:
            argVal = argDict[argKey]
            if argVal is not None:
                if argKey != 'specialDict':
                    getDataDict[argKey] = argVal
                # 对于非正常格式的get参数单独兼容
                else:
                    specialDict = argVal
        if specialDict is not None:
            getDataDict = dict(getDataDict, **specialDict)
        return self.__getOne(reqHost, uri, getDataDict)

    def postRequest(self, reqHost, uri, **args):
        postDataDict = {}
        specialDict = None
        argDict = args
        for argKey in argDict:
            argVal = argDict[argKey]
            if argVal is not None:
                if argKey != 'specialDict':
                    postDataDict[argKey] = argVal
                    # 对于非正常格式的post参数单独兼容
                else:
                    specialDict = argVal
        if specialDict is not None:
            postDataDict = dict(postDataDict, **specialDict)
        return self.__postOne(reqHost, uri, postDataDict)

if __name__=="__main__":
    # 处理get，post请求时候使用，后续具体场景需要优化
    pass
