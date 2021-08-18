import numpy as np
data = np.random.randint(0, 200)

count = 0
coin = 2000
while coin > 0:
    num = input("请输入您要猜的整数:")
    num = int(num)
    count = count + 1
    if num < data:
        print("小了！")
        coin = coin - 200
        print("剩余金币数：", coin)
        pass
    elif num > data:
        print("大了！")
        coin = coin - 200
        print("剩余金币数:", coin)
        pass
    elif num == data:
        print("恭喜，猜中了！本次幸运数字为：", data, "，本次猜了", count, "次！")
        again = input("是否继续游戏？请输入yes或者no：")
        if again == "yes":
            coin = coin + 5000
            count = 0
            data = np.random.randint(0, 200)
            print("剩余金币数：", coin)
            pass
        elif again == "no":
            break
        else:
            print("输入非法")
            break
        pass
    else:
        print("输入非法")
        break
    pass
