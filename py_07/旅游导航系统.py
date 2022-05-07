# author:jason
'''
    任务1：
        将导航系统与商城系统结合一起。
'''
data = {
    "北京":{
        "昌平":{
            "十三陵":["十三陵水库","沙河水库"],
            "高校":["北京邮电大学","中央戏剧学院","北京师范大学","华北电力大学","北京航空航天大学"],
            "天通苑":["海底捞","呷哺呷哺"]
        },
        "海淀":{
            "公主坟":["军事博物馆","中华世纪园"],
            "科普场馆":["中国科技馆","北京天文馆"],
            "高校":["北京大学","清华大学"],
            "景区":["北京植物园","香山公园","玉渊潭公园"]
        },
        "朝阳":{
            "龙城":["鸟化石国家地质公园","朝阳南北塔"],
            "双塔":["朝阳凌河公园","朝阳凤凰山"]
        },
        "延庆":{
            "龙庆峡":["龙庆峡景区"]
        }
    }
}

# 打印城市
def print_place(choice):
    for i in choice:
        print(i)

# 攻略
for i in data:
    print(i)


while True:
    city1 = input("请输入您要去的城市：")
    if city1 in data:
        print_place(data[city1])
        city2 = input("亲输入二级城市：")
        if city2 in data[city1]:
            print_place(data[city1][city2])
            city3  = input("亲输入三级地区：")
            if city3 in data[city1][city2]:
                print_place(data[city1][city2][city3])
                # 商城系统


        else:
            print("当前二级城市不存在，别瞎弄！")
    elif city1 == 'q' or city1 == "Q":
        print("------------------欢迎下次光临Jason旅行社！------------------")
        break
    else:
        print("当前城市不存在，别瞎弄！")

























