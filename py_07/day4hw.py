import numpy as np
from copy import deepcopy

shop = [["劳力士手表", 200000],
        ["Iphone 12X plus", 12000],
        ["lenovo PC", 6000],
        ["HUA WEI WATCH", 1200],
        ["Mac PC", 15000],
        ["辣条", 2.5],
        ["老干妈", 13]]

shop_copy = deepcopy(shop)

discount_num1 = 6
discount1 = 0.7
discount_num2 = 2
discount2 = 0.1

for i in range(3):
    data = np.random.randint(1, 30)
    chose1 = input("请选择是否参加优惠券抽奖活动？输入yes或no：")
    if chose1 == "yes":
        if data <= 10:
            print("恭喜您抽到了 老干妈7折优惠券！")
            discount = discount1
            discount_num = discount_num1
            break
        else:
            print("恭喜您抽到了 lenovo PC 1折优惠券！")
            discount = discount2
            discount_num = discount_num2
            break
        pass
    elif chose1 == "no":
        break
    else:
        print("输入错误，请重新输入！")
        pass

balance = input("请输入您的余额：")
balance = int(balance)

mycart = []
count = -1

for i in range(20):
    for key, value in enumerate(shop):
        print(key, value)
        pass

    chose2 = input("请输入您想购买的商品编号:")
    if chose2.isdigit() is True:
        chose2 = int(chose2)
        if chose2 > 6:
            print("您输入的商品不存在，请重新输入！")
            pass
        else:
            if balance < shop[chose2][1]:
                print("您的余额不足，请充值后再购买!")
                pass
            else:
                mycart.append(shop_copy[chose2])
                count = count + 1
                price = shop_copy[chose2][1]
                if discount_num == chose2:
                    for i in range(3):
                        chose3 = input("您有一张该商品的优惠券，是否要使用？输入yes或no:")
                        if chose3 == "yes":
                            balance = balance - price*discount
                            mycart[count][1] = price*discount
                            discount_num = -1
                            discount = -1
                            print("使用成功！")
                            break
                        elif chose3 == "no":
                            break
                        else:
                            print("输入错误，请重新输入！")
                            pass
                        pass
                    pass
                balance = balance - price
                print("购买成功，当前余额为：", round(balance, 1))
                pass
            pass
        pass
    elif chose2 == "q" or chose2 == "Q":
        print("欢迎下次光临！")
        break
    else:
        print("输入错误，请重新输入！")
        pass
    pass

print("以下是您的购物小条，请拿好：")
for key, value in enumerate(mycart):
    print(key, value)
    pass
print("本次余额还剩：￥", round(balance, 1))
