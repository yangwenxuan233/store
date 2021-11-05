import numpy as np

# 矩阵的运算 N*M M*K ->N*K
arr1 = np.array([[1,2,3],[4,5,6]])
print(arr1.reshape(3,-1))  # 三行 xx列 视数组情况而定
arr2 = np.array([[1,2],[3,4],[5,6]])
print(arr1.dot(arr2))
print(np.dot(arr1,arr2))

# 补充 其他函数和广播机制

print(np.linspace(1,10,5))
print(np.linspace(1,10,5,endpoint=False))
print(np.logspace(1,4,4))    # [10,100,1000,10000]
print(np.logspace(1,4,4,base=2))

# 扩维
array1d = np.array([1,2,3,4,5])
# array1d = np.array([[1],[2],[3],[4],[5]])
print(array1d[:,np.newaxis])
print(array1d[np.newaxis,:])

# flatten 拉平
print(arr1.flatten())

arr3 = np.array([[7,8,9]])
print(np.concatenate((arr1,arr3),axis=0))
print(np.vstack((arr1,arr3)))

# 广播机制
arr1 = np.array([[1,2,3],[4,5,6]])
arr2 = np.array([1,2,3])
print(arr1 + arr2)   # 列数相同  按行相加
arr3 = np.array([[1],[3]])  # 行数相同 按列相加
print(arr1 + arr2)
print(arr1 + arr3)

# 倒序访问
print(arr2[::-1])
print(arr2[3:1:-1])  # 初始下标比终点下标大

