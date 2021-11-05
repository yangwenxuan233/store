data = input("请输入数字，用逗号隔开：").split(",")
list1 = [int(i) for i in data]
list1.sort()
print(list1)

goodsList = [{'id': 1, 'name': 'apple', 'price': 10}, {'id': 2, 'name': 'orange', 'price': 8}]
g = {}
for t in goodsList:
    if t['id'] == 2:
        g = t
        pass
    if t['id'] == 1:
        t['price'] == 10
        pass
    pass
goodsList.remove(g)
print(goodsList)
