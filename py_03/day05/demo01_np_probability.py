import numpy as np

x = np.array([1,2,3,4])
y = np.array([1,12,3,4])

print(x-np.mean(x))
print(np.sum(x-np.mean(x)**2)/len(x))
print(np.var(x))  # 方差
print((np.sum((x-np.mean(x))**2)/len(x))**0.5)
print(np.std(x))  # 标准差

print(np.sum((x-np.mean(x))*(y-np.mean(y)))/len(x))
print(np.cov(x,y,ddof=0))  # ddof=0 有偏差  ddof=1 无偏差
# 相关性
# [自己跟自己的相关，自己跟其他的相关
#  自己跟其他的相关，自己跟自己的相关]

A = np.array([x,y])
print(np.corrcoef(A,ddof=0))

x = np.array([1,2])
y = np.array([-1,-2])
print(np.corrcoef(x,y,ddof=0))
