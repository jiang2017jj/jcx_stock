import json
from unittest.util import safe_repr
import logging

# 断言类
class AssertHandler():
    def __init__(self):
        pass

    # 检查接口的response 中的Dict的key是否符合预期
    def assertDictKeyEqual(self,expected, actual, msg=""):
        expected = json.loads(expected)
        actual = json.loads(actual)
        missing = []
        try:
            if expected and actual:
                for key in expected.keys():
                    if key not in actual.keys():
                        missing.append(key)
                if not missing:
                    return None
                else:
                    standardMsg = 'Missing: %s' % ','.join(safe_repr(m) for m in missing)
                    msg = msg + standardMsg
            return msg
        except Exception as e:
            print(e)
            return None


    # 检查list的每一项item是否符合预期:item为key-value类型
    def assertListItemEqual(self,expected,actual,msg=""):
        pass


    # 精确检查两个list列表是否相同,要求两个长度必须相同
    def assertListKeyAndValueEqual(self,testClass,expected,actual,msg=""):
        pass


    def calculate_theta(self,sum_alpha):
        """
        :key: 初始化并计算模型的theta值(M*K),用到alpha值
        """
        theta = 0
        # 断言可以作为函数语句呢。。。。。。
        assert sum_alpha > 0
        theta = sum_alpha
        # 如果return后面什么都不加，默认返回None
        return theta



if __name__ == "__main__":
    # 测试的时候把日志也打出来，更好！！！
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
