import pandas as pd
import numpy as np

# series
s1 = pd.Series([1,2,3,4,5],index=['a','b','c','d','e'])
print(s1)

s2 = pd.Series([1,2,3,4,5])
print(s2)

print(s1['a'])
s3 = s1.drop('a')
print(s3)
print(s1**2)
print(np.exp(s1))

s4 = pd.Series([2,3,4],index=['a','c','f'])
print(s1 + s4)  # 索引相同时直接计算 找不到相同时用缺失值NAN
s5 = s1 + s4
print(pd.notnull(s1 + s4))
print(s5[pd.notnull(s1 + s4)])


