# 函数与函数参数
def sum1(x, y):
    return x+y


result = sum1(1, 2)
print(result)

# 带默认值的参数
def test(x, y, z=10):
    return x+y+z
    pass


result = test(10, 20)   # z使用了默认值
print(result)

result = test(10, 20, 30)
print(result)

result = test(y=1, x=3, z=100)

# 可变的参数
def test1(x, y, *args):
    print(args)
    r = x + y
    for t in args:
        r += t
        pass
    return r

result = test1(1,2,3,4,5,6,7,8,9)
print(1,2,3,4,5,sep='-')

def test2(x,y,**kw):  # key value 的不定长参数
    print(kw)  # kw是一个字典
    return x+y+kw['k']

# 固定参数 * k=v **kw (参数顺序）
r = test2(10,20,k=30,k2=40,k3=50,k4=60)
print(r)

class Animal(object):
    type = '犬类'  # 类属性



    # 构造方法
    def __init__(self, name="",age=0):  # 没有重载 只能覆盖 self==this 代表当前对象
        print('构造方法被调用了！')
        self.name = name    # self.生成的属性 构成实体属性
        self.age = age
        self.__money = 0   # 两个下划线的属性是私有属性 private
        self._weight = 11  # 保护类型 protect 和公有差不多
        pass

    # 成员方法
    def eat(self,food):
        print(self.name + "吃：" + food)
        pass
    @classmethod  # 装饰器
    def classMtd(cls):
        print(Animal.type)
        print(cls.type)
        pass

    @staticmethod
    def staticMtd():
        pass

    def getMoney(self):
        return self.__money
    pass
    def __setMoney(self):

        pass

    pass
dog = Animal('二哈', 5)
print(dog.name)
dog.eat("大棒骨")
dog2 = Animal('布丁', 3)
print(dog.type)
print(dog2.type)

# 访问控制 print(dog.__money) 私有属性在类外部不能访问
print(dog.getMoney())


# 继承 重载 python没有重载
def sum2(x, y):
    pass

def sum2(x):
    pass

sum2(10)

# python 支持多继承和多重继承
class Dog(Animal):

    def eat(self,food):
        print(self.name + "吃：" + food)
        pass
    pass

class Cat(Animal):
    def eat(self, food):
        print(self.name + '1' +food)
        pass
    pass

class Monster(Dog, Cat):
    pass

dog = Dog('京巴', 11)
dog.eat('bone')

m = Monster('四不像', 1)
m.eat('---')
print(Monster.mro())   # C3算法
