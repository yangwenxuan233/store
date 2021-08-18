from collections import Counter

f = open(r"D:\pscode\demo\day15hw\baidu_x_system.log", mode="r+", encoding="utf-8")

# 按行遍历，按空格分割字符，取得所有行首ip地址
# data = f.readlines()
# list = [i.split(" ") for i in data]
# ip = [i[0] for i in list]
ip = [i[0] for i in [i.split(" ") for i in f.readlines()]]
print(ip)

# 统计ip出现次数
print(Counter(ip))
