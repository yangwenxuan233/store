'''
          人：
            姓名，年龄，性别
            吃，喝，睡觉，学
    2.封装
        2.1 将属性进行隐藏，为了在类外不能直接看见
            __xxx
        2.2 对每个属性提供setxxxx/getXXX方法，间接的赋值，取值
            def setXxxx(xxx):
                self._xxx = xxx
            def getXxxx():
                return self.__xxx

'''
class Person:
    __username = ""
    __age = 0
    __sex = ""

    def setUsername(self,username):
        self.__username = username

    def getUsername(self):
        return self.__username

    def setAge(self,age):
        if age < 0  or age > 100:
            print("对不起，输入非法！")
        else:
            self.__age = age

    def setSex(self,sex):
        self.__sex =  sex

    def eat(self,eatname):
        print(self.__username,"正在吃",eatname)

    def drink(self,drink):
        print(self.__username,"正在喝",drink)

    def sleep(self,hour):
        print(self.__username , "已经睡了",hour,"个小时！")

    def study(self,hour):
        print(self.__username,"正在学习，已经学了",hour,"个小时！")

    def showMe(self):
        print("我叫",self.__username,",我今年",self.__age,",我是",self.__sex)

p = Person()
# p.username = "纪博文"
p.setUsername("纪博文")
# p.sex = "male"
p.setSex("male")
# p.age = -90
p.setAge(-90)

p.drink("农夫山泉")
p.eat("小汉堡")
p.sleep(10)
p.study(5)
p.showMe()

print(p.getUsername())















