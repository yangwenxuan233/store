class Oldphone:
    __type = ""

    def setType(self, type):
        self.__type = type

    def getType(self):
        return self.__type

    def call(self, phonenum):
        print("正在给", phonenum, "打电话")


class Newphone(Oldphone):

    def call(self, phonenum):
        print("语音拨号中...")
        super().call(phonenum)

    def show(self):
        print("品牌为", super().getType(), "的手机很好用")


class Test_phone():
    phone = Newphone()
    phone.setType("华为")
    phone.show()
    phone.call("17778885125")


class Chef():

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def setAge(self, age):
        self.__age = age

    def getAge(self):
        return self.__age

    def steam(self):
        print("蒸 饭 中...")


class Chef_son(Chef):

    def fry(self):
        print("炒 菜 中...")


class Chef_grandson(Chef_son):

    def steam(self):
        print("正在蒸饭...")

    def fry(self):
        print("正在炒菜...")


class Test_chef():
    grandson = Chef_grandson()
    grandson.setName("张三")
    grandson.setAge("20")
    print("厨师", grandson.getName(), "今年", grandson.getAge())
    grandson.steam()
    grandson.fry()


class Person():
    __name = ""
    __sex = ""
    __age = ""

    def setName(self, name):
        self.__name = name

    def setSex(self, sex):
        self.__sex = sex

    def setAge(self, age):
        self.__age = age

    def getName(self):
        return self.__name

    def getSex(self):
        return self.__sex

    def getAge(self):
        return self.__age


class Worker(Person):

    def work(self):
        print("正在干活...")


class Student(Person):
    __id = ""

    def setId(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def study(self):
        print("正在学习...")


class Test_person():
    worker = Worker()
    student = Student()
    worker.work()
    student.study()
