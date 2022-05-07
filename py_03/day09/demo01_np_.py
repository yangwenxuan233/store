import numpy as np

# 行向量
rowVector = np.array([1,2,3,4,5])
rowVector1 = np.array([[1,2,3,4,5]])
print(rowVector)
cVector = rowVector.T
print(cVector)  # 无效
cVector = rowVector1.T
print(cVector)
cVector = rowVector[:,np.newaxis]  # 扩维
print(cVector)

# numpy特殊处理   便于写公式
A = np.array([[1,2,3],
                  [4,5,6]])
x = np.array(([1,2,3]))
print(A.dot(x))  # 默认： x=np.array([[1],[2],[3]])

print(A.dot(np.array([[1],[2],[3]])))

# 将一个列向量和一个行向量运算

xc = np.array([[1],[2],[3]])  # 3*1
print(x[np.newaxis,:])
print(xc.dot(x[np.newaxis,:])) # 1*3