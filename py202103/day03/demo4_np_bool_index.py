import numpy as np

# 布尔索引
# 找出一组数里所有的偶数
array1d = np.arange(1,21,1)
print(array1d)
boolArray = (array1d % 2 == 0)
print(boolArray)
print(array1d[boolArray])

# 简写
print(array1d[array1d % 2 == 0])

array1d = np.array([1,23,4,20])
print(array1d[[True, False, True,True]])

result = []
for x in array1d:
    if x % 2 == 0:
        result.append(x)
        pass
pass
print(result)

print(array1d[(array1d % 2 == 0) & (array1d > 10)])

# 多维选取
array2D = np.arange(1,21,1).reshape(4,5)
print(array2D[array2D > 10])

# 花式索引
array2D = np.array([[1,2,3,4],
                    [11,12,13,14],
                    [22,23,24,25],
                    [22,23,11,11]])
print(array2D[[1,2]])
print(array2D[[1,2],[1,2]])  # array2D([行花式],[列花式])


