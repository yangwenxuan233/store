import pandas as pd
import numpy as np
# dataframe--numpy里的二维数组

df1 = pd.DataFrame([[1,2,3,4,5],[6,7,8,9,10]],index=[1,2],columns=['x','y','z','m','n'])
# index 行索引 columns 列索引
print(df1)
print(df1 + df1)
print(df1 - df1)
print(df1 / df1)
print(df1 * df1)
print(df1**2)
print(np.exp(df1))

df2 = pd.DataFrame([[1,2,3,4,'5'],[6,7,8,9,10]],index=[1,2],columns=['x','y','k','m','n'])
print(df2)  # 可以允许数组里的值类型不一致

df3 = pd.DataFrame([[1,2,3,4],[6,7,8,9]],index=[1,2],columns=['x','y','z','m'])
print(df2 + df3)
print(df3['x'][1])  # 先列后行

df3['k'] = pd.Series([1,2],index=[1,2])  # 给不存在的列赋值 则新增一个列
print(df3)
print(df3.drop(['x'],axis=1))  # axis=1 删列 axis=0 删行
print(df3.drop([1],axis=0))

df3.to_csv('a.csv')
df = pd.read_csv('a.csv')
print(df)

df3.to_excel('a.xls')
df = pd.read_excel('a.xls')
print(df)

print(df.describe())  # 统计数据
