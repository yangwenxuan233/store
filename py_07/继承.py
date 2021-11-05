'''
    继承：
        父与子
        父类与子类的关系。
    被继承的类：父类，超类
    继承的类：子类
    好处：
        新代码任然可以使用旧的代码
        可以提高旧代码的可复用性
        子类可以任意扩展父类的代码
'''
class Animal:
    username = ""
    age = 0

class Dog(Animal):
    pass

class Cat(Animal):
    def catchMouse(self):
        pass
    pass

class Turkey(Animal):
    pass

class Donkey(Animal):
    pass

























