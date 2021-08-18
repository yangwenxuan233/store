import random
import time


class Addresss():
    __country = ""
    __province = ""
    __street = ""
    __door = ""

    def __init__(self, country, province, street, door):
        self.__country = country
        self.__province = province
        self.__street = street
        self.__door = door

    def setCountry(self,  country):
        self.__country = country

    def getCountry(self):
        return self.__country

    def setProvince(self, province):
        self.__province = province

    def getProvince(self):
        return self.__province

    def setStreet(self, street):
        self.__street = street

    def getStreet(self):
        return self.__street

    def setDoor(self, door):
        self.__door = door

    def getDoor(self):
        return self.__door


class Student(Addresss):
    __idcard = ""
    __name = ""
    __sex = ""
    __age = 0
    __password = ""  # 6-12位数
    __status = True  # True活着，False死亡
    __regist_date = time.strftime("%Y-%m-%d")  # 注册日期默认获取
    __emigrant_date = None  # 移民日期默认为空

    def setIdcard(self):
        randchar = ""
        for i in range(32):
            num = random.randint(0, 9)
            # num = chr(random.randint(48,57)) # ASCII取数字
            letter = chr(random.randint(97, 122))  # 取小写字母
            Letter = chr(random.randint(65, 90))  # 取大写字母
            s = str(random.choice([num, letter, Letter]))
            randchar += s
        self.__idcard = randchar

    def getIdcard(self):
        return self.__idcard

    def setName(self, name):
        self.__name = name

    def getNameu(self):
        return self.__name

    def setSex(self, sex):
        self.__sex = sex

    def getSex(self):
        return self.__sex

    def setAge(self, age):
        self.__age = int(age)

    def getAge(self):
        return self.__age

    def setPassword(self, password):
        if len(password) <= 12 and len(password) >= 6:
            self.__password = password

    def getPassword(self):
        return self.__password

    def setStatus(self, status):
        self.__status = status

    def getStatus(self):
        return self.__status

    def getRegist_data(self):
        return self.__regist_date

    def setEmigrant_data(self, emigrant_data):
        self.__emigrant_date = emigrant_data

    def getEmigrant_data(self):
        return self.__emigrant_date

    
