#!/usr/bin/env python3
#-*- coding = utf-8 -*-

# 涉及到了methodtype，slots，init，super等很多知识点

from types import MethodType

#  __slots__只对当前类起作用，对子类不起作用
# 除非在子类中也定义__slots__，这样，子类实例允许定义的属性就是自身的__slots__加上父类的__slots__。
class Dog(object):
    # __slots__必须是一个元组，而不是写在一起的字符串
    # __slots__ = 'name,age,color'
    __slots__ = 'name','age','color'

    # 此时传参如果有city，那么就会报错
    def __init__(self,name,age,color):
        self.name = name
        self.age = age
        self.color = color

    def get_info(self):
        return self.name


class GuiFu(Dog):
    # 子类一旦定义了__slots__，父类的__slots__里面的也跟着生效！！！
    # 这里没有包含weight，父类也没有包含weight，运行要报错的,
    # 这里不加set_name，后续运行guifu.set_name = MethodType(set_name,guifu)的时候，会报错AttributeError: 'GuiFu' object has no attribute 'set_name';
    __slots__ = 'haha','lala','weight','set_name'

    # 这涉及到了另一个关于__init__的知识点，当子类不定义__init__方法时，子类会自动调用父类的__init__方法，
    # 当子类也有__init__方法的时候，相当于重写了父类的__init__方法，此时就不会调用父类的__init__了
    # 但是为了更好的继承父类和拓展父类功能，最好能显示调用父类的__init__
    # 子类的__init__中要有父类的__init__的参数列表+自己的参数列表
    def __init__(self,name,age,color,weight):
        # 显示的调用父类的__init__方法，可以使用两种方法：
        # 如果是单继承，Dog.__init__(name,age,color)
        # 如果是多继承，super(GuiFu,self).__init__(name,age,color)
        # 综上，直接使用super类调用父类的__init__就行了，单多通吃，参数是父类的__init__的参数，self不写，因为这已经是调用，不是定义了
        # 而且在python3中super（）不用写参数也可以。
        super(GuiFu,self).__init__(name,age,color)
        # Python3.x 和 Python2.x 的一个区别是: Python 3 可以使用直接使用 super().xxx 代替 super(Class, self).xxx
        # super().__init__(name, age, color)
        # Dog.__init__(name, age, color)
        self.weight = weight


    def get_info(self):
        return self.weight


def set_name(self,name):
    self.name = name

def set_hehe(self):
    self.hehe = 99



# 使用Python自带的property方法。做什么用呢？可以将函数变为属性那么调用。
class Person(object):

    def __init__(self):
        self._name = None
        return

    def get_name(self):
        print("get_name")
        return self._name

    def set_name(self, name):
        print("set_name")
        self._name = name
        return

    name = property(fget=get_name, fset=set_name, doc="person name")


# 也可以这样用，使用Python自带的装饰器 @property
class People(object):

    def __init__(self):
        self._name = None
        self._age = None
        return

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        return

    @name.deleter
    def name(self, name):
        del name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        assert 0 < age < 120
        self._age = age
        return

    @age.deleter
    def age(self, age):
        assert 0 < age < 120
        del age





"""
类中普通的实例方法第一个参数默认是对象本身，即需要是self,self表示是 对象 自身,实例方法只能被实例对象调用；

如果使用了@staticmethod修饰，则参数可以任意，可以无视这个self，而将这个方法当成普通方法使用，可以被 类 或 类的实例 调用，

为啥要有静态方法呢？因为python只能有一个初始化方法，所以有了静态方法是为了模仿java按照不同情况进行初始化；

如果使用了@classmethod则第一个参数不是self，而是cls，它表示这个 类 本身，由类直接调用，可以用于新建对象；

python继承中，子类继承父类，而且子类重写了父类的静态方法，类方法：

子类的实例继承了父类的static_method方法，调用静态方法，调用的还是父类的静态方法？验证过了并不是，是子类的。

如果是父类的实例化对象，调用静态方法，那肯定还是父类的静态方法。子类只是在自己那重写了，并不能将父类的静态方法覆盖。

子类的实例继承了父类的class_method方法，调用该方法，调用的是子类的方法和子类的类属性。

同理，父类的实例调用类方法，肯定是自己的类方法，不是子类的类方法。
"""
class Foo(object):
    # 类常量
    X = 1
    Y = 14
    def __init__(self,a,b):
        self.a = a
        self.b = b

    # 静态方法
    @staticmethod
    def averag(*mixes):
        # 返回mixes的长度
        print("这是父类中的averag方法")
        return sum(mixes)

    # 静态方法
    @staticmethod
    def static_method():
        print("父类中的静态方法static_method")
        return Foo.averag(Foo.X,Foo.Y)

    # 类方法
    @classmethod
    def class_method(cls):
        print("父类中的类方法：class_method")
        return cls.averag(cls.X,cls.Y)


class Son(Foo):
    X = 3
    Y = 5
    def __init__(self,a,b,c):
        super().__init__(a,b)
        self.c = c

    # 子类中重载了父类的静态方法
    @staticmethod
    def averag(*mixes):
        print("这是子类中重载了父类的静态方法")
        return sum(mixes)




QA = ['a','b']

# 静态方法什么作用？可以定制化类的实例对象
# 字典在代码中的作用，一般是用来当新字典的key或者更新这个字典
@staticmethod
def classify_by_department(issues):
    """
    :param issues:
    :return:
    """
    department = {
        '基础服务': 0,
        '保险服务': 0,
        '财商基金': 0,
        '保险供应链': 0
    }
    for issue in issues:
        if issue['business'] == 'FNDN':
            department['基础服务'] += 1
        if issue['business'] == 'INSU':
            department['保险服务'] += 1
        if issue['business'] == 'FQ':
            department['财商基金'] += 1
        if issue['business'] == 'INSC':
            department['保险供应链'] += 1

    return department




# 关于下划线的验证说明，部分代码用得到，尤其是想隐藏某些属性的时候
class A:
    def _a(self):
        return '单下滑线'
    def __b(self):
        return '双下划线'
    def __c__(self):
        return '前后双下划线'

    # 这样调用可以成功调用__X()这种方法
    def bb(self):
        return self.__b()

class B(A):
    def __init__(self):
        super().__init__()  #调用父类的__init__方法






if __name__=="__main__":
    dog = Dog('ww',1,'red')
    # dog.birthday = '2020-01-12'
    # print(dog.birthday)
    print(dog.get_info())

    # # 注意：与python2相比MethodType()只接收两个参数，即去掉了所属类的参数
    # dog.set_name = MethodType(set_name,dog)
    # dog.set_name('sb')
    # print(dog.name)
    #
    # Dog.set_hehe=MethodType(set_hehe,Dog)
    # # Dog和dog都能调用.hehe。。。。。。太危险了
    # # Dog.set_hehe()
    # dog.set_hehe()
    # print(dog.hehe)
    # __slots__对子类没作用，如果想起作用，则子类需要也定义__slots__
    guifu = GuiFu('dog1',1,'red','2')
    guifu.set_name = MethodType(set_name,guifu)
    guifu.set_name('sb')
    print(guifu.name)


    # 实例化后都实现了新建类属性的目的，可以让类名.属性名 这样调用
    myperson = Person()
    mypeople = People()
    myperson.name = 'jcl'
    print(myperson.name)
    mypeople.name = 'jcx'
    print(mypeople.name)



    # 静态方法，类方法
    p = Son(1, 2, 3)
    # 应该调用父类中的静态方法，为啥调用的是子类中的呢？
    print(p.averag(1, 5))
    # print(p.static_method())
    # print(p.class_method())


    # 私有属性
    a = A()
    print(a._a())         #单下滑线
    # print(a.__b())      # 报错
    print(a.__c__())      #前后双下划线
    print (a.bb())        #双下划线

    b = B()
    print(b._a())        #单下滑线
    # print(b.__b())     # 报错
    print(b.__c__())     #前后双下划线
    print(b.bb())        #双下划线



