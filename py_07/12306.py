'''
    需求： 500张票
        4个人同时抢500张票。
    分析：同时做事情，人实现多线程。
        每个人的任务：抢票
'''
from threading import Thread
import time

ticket = 1000 # ticket票


class Person(Thread):
    username = ""
    count = 0
    def run(self) -> None:
        global ticket
        while True:
            if ticket > 0:
                self.count = self.count + 1
                ticket = ticket - 1
                print(self.username,"成功抢了一张票，还剩",ticket ,"张票！")
            else:
                print(self.username,"总共抢了",self.count,"张！")
                break

p1 = Person()
p2 = Person()
p3 = Person()
p4 = Person()

p1.username = "纪博文"
p2.username = "旺财"
p3.username = "二哈"
p4.username = "金毛"

p1.start()
p2.start()
p3.start()
p4.start()








