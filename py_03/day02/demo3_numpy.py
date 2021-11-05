import numpy as np
array = np.array([1,2,3,4,5])
print(type(array))

# 定义多维数组 numpy数组与c语言数组是一样的，数据类型要一致
array2D = np.array([[1,2,3,4,5],[6,7,8,9,10]])
array3D = np.array([[[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]], dtype=np.int)
print(array2D)
print(array3D)

print(array3D.shape)
print(array3D.dtype)

# 特殊数组
print(np.zeros(shape=(4,5)))
print(np.zeros(shape=(4,)))
print(np.ones(shape=(5,5)))
print(np.identity(8))   # 8*8单位方阵
print(np.eye(4,5))   # 主对角线为1 不一定是方阵
print(np.sign(100))  # 判断正负零
print(np.diag([1,2,3,4,5]))  # 形成矩阵的对角线元素

# arange生成器 生成numpy数组  reshape一起使用
array1D = np.arange(1, 21, 1)   # 不包含上界
print(array1D)

print(array2D.reshape(5,2))

print(np.arange(1,21,1).reshape(4,5))
print(np.arange(1,21,1).reshape(2,2,5))

floatArray = array1D.astype(dtype=np.float)
print(floatArray)

# 矢量化计算
array2d = np.arange(1,21,1).reshape(4,5)
print(array2d + array2d)
print(array2d - array2d)
print(array2d * array2d)
print(array2d / array2d)
print(array2d+1)
print(array2d**2)
print(np.sqrt(array2d))

for row1,row2 in zip(array2d, array2d):
    for x1,x2 in zip(row1,row2):
        z = x1 + x2
        pass
    pass

# 索引和切片
array1d = np.arange(1,11,1)
print(array1d[0])
print(array1d[5::1])
array1d[5::1] = 10
print(array1d)
array1d[:] = 0  # 浅拷贝 会改变原数据的值
print(array1d)
arr = array1d.copy()  # 深拷贝 不会改变array1d
arr[:] = 1
print(arr)
print(array1d)

array2D = np.array([[1,2,3,4,5],[6,7,8,9,10]])
print(array2D[0::1,2::1])
print(array2D[0::1,2::2])


# and or not

x = 10
if x > 10 and x < 100:
    pass
if x > 10 or x < -10:
    pass
