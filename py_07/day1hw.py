import pandas as pd
import numpy as np

ex = pd.read_excel('12月份衣服销售数据.xlsx')

a = np.array(ex['价格/件'].values)
b = np.array(ex['销售量/每日'].values)
c = np.array([[a], [b]])
print(c)

totalsell = a * b  # 月度总销售额
print(totalsell)

print("12月份销售总金额\n", round(totalsell.sum(axis=0), 1))

totalcount = b.sum(axis=0)  # 月度总销售量

count1 = np.array(b[[0, 7, 9, 16, 27]])
sell1 = np.array(totalsell[[0, 7, 9, 16, 27]])  # 羽绒服

count2 = np.array(b[[1, 6, 8, 10, 14, 19, 23]])
sell2 = np.array(totalsell[[1, 6, 8, 10, 14, 19, 23]])  # 牛仔裤

count3 = np.array(b[[2, 13, 17, 21, 25, 29]])
sell3 = np.array(totalsell[[2, 13, 17, 21, 25, 29]])  # 风衣

count4 = np.array(b[[3, 11, 20, 26]])
sell4 = np.array(totalsell[[3, 11, 20, 26]])  # 皮草

count5 = np.array(b[[4, 12, 15, 18, 22, 24, 28]])
sell5 = np.array(totalsell[[4, 12, 15, 18, 22, 24, 28]])  # T恤

count6 = np.array(b[[5]])
sell6 = np.array(totalsell[[5]])  # 衬衫

print("羽绒服销售数量占比", round((count1.sum(axis=0)/(totalcount))*100, 2), "%")
print("牛仔裤销售数量占比", round((count2.sum(axis=0)/(totalcount))*100, 2), "%")
print("风衣销售数量占比", round((count3.sum(axis=0)/(totalcount))*100, 2), "%")
print("皮草销售数量占比", round((count4.sum(axis=0)/(totalcount))*100, 2), "%")
print("T恤销售数量占比", round((count5.sum(axis=0)/(totalcount))*100, 2), "%")
print("衬衫销售数量占比", round((count6.sum(axis=0)/(totalcount))*100, 2), "%")

print("羽绒服销售额占比", round((sell1.sum(axis=0)/(totalsell.sum(axis=0)))*100, 2), "%")
print("牛仔裤销售额占比", round((sell2.sum(axis=0)/(totalsell.sum(axis=0)))*100, 2), "%")
print("风衣销售额占比", round((sell3.sum(axis=0)/(totalsell.sum(axis=0)))*100, 2), "%")
print("皮草销售额占比", round((sell4.sum(axis=0)/(totalsell.sum(axis=0)))*100, 2), "%")
print("T恤销售额占比", round((sell5.sum(axis=0)/(totalsell.sum(axis=0)))*100, 2), "%")
print("衬衫销售额占比", round((sell6.sum(axis=0)/(totalsell.sum(axis=0)))*100, 2), "%")
