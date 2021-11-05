import numpy as np

# 轴转换
array2d = np.array([[1,2,3,4],
                   [5,6,7,8]])   # 2*4 由两个4个元素的一位数组 组成了一个2*4的二维数组
print(array2d)
print(array2d.T)
# transpose(0,1,2)
print(array2d.transpose(1, 0))

# 三维数组
# array3d[x][y][z]     取第x个二维数组的第y行的第z个元素  （下标从0开始)
array3d = np.arange(1,21,1).reshape(2,2,5)
print(array3d)
print(array3d[0][0][0])
print(array3d.transpose(2,1,0))




