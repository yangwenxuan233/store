import time
from threading import Thread

bread = 0
price = 2


class Chef(Thread):
    def run(self) -> None:
        global bread
        while True:
            if bread >= 600:
                time.sleep(0.5)
            else:
                bread = bread + 1
                time.sleep(0.5)
                print("篮子里现在有", bread, "个面包")


class Customer(Thread):
    money = 3000
    count = 0
    name = ""

    def __init__(self, name):
        self.name = name

    def setName(self, name):
        self.name = name

    def run(self) -> None:
        global bread
        global price
        while True:
            if bread < 1:
                time.sleep(1)
            elif bread >= 1 and self.money >= price:
                bread = bread - 1
                self.money = self.money - price
                self.count = self.count + 1
                print(self.name, "抢到了一个面包，当前余额", self.money)
            elif self.money < price:
                print(self.name, "余额不足，一共抢到了", self.count, "个面包")


c1 = Chef()
c2 = Chef()
c3 = Chef()

b1 = Customer()
b1.setName("1号顾客")
b2 = Customer()
b2.setName("2号顾客")
b3 = Customer()
b3.setName("3号顾客")
b4 = Customer()
b4.setName("4号顾客")

c1.start()
c2.start()
c3.start()

b1.start()
b2.start()
b3.start()
b4.start()
