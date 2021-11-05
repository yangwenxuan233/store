'''
    猜数字游戏：
        需求：
            1.系统产生一个随机数，
            2.用户从键盘输入数据，与随机数进行比对
                2.1 若大了，温馨提示：大了
                2.2 若小了，提示：小了
                2.3 提示：恭喜您，猜中！

        技术选型：
            1.随机数技术
                import random
                random.randint(开始数据，结束数据)
            2.键盘输入技术
                name = input()
            3.判断技术：多分支判断
                if....else
                if...elif.....elif....else
            4.循环技术
                while 条件：
    任务：
        加上金币赌博功能。
            初始化有2000金币，没猜错一次，扣200金币。
            10机会，钱扣完为止。
            在机会过程中，若猜中，奖励5000金币。
            然后询问，是否继续？是，否。
'''
import random
# 1. 让系统产生一个随机数
data = random.randint(0,200) # 22

count = 0
# 2.循环的让用户去猜
i = 1
while i <= 5:
    count = count + 1
    num = input("请输入您要猜的数字：")# "22"   "23"
    num = int(num) # "22"  -->  22
    if num > data:
        print("大了！")
    elif num < data:
        print("小了！")
    else:
        print("恭喜，猜中了！本次幸运数字为：",data,"，本次猜了",count,"次！")
        break  # 终止循环
    i = i + 1
