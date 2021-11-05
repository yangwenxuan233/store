import numpy as np
# 二进制的存储和读取，不能保存形状
array2d = np.arange(1,21,1).reshape(4,5)
print(array2d)
array2d.tofile('a.bin')
array = np.fromfile('a.bin',dtype=np.int)
print(array)

# npy 可以还原
np.save('a.npy',array2d)
array = np.load('a.npy')
print(array)
print(array.shape)
print(array.dtype)

# npz
c = np.array([[1.0,2.0,3.0]],dtype=np.float)
np.savez('a.npz', array2d, array, arrc = c)
arrs = np.load('a.npz')
print(arrs['arr_0'])
print(arrs['arr_1'])
print(arrs['arrc'])

# csv通用数据格式
np.savetxt('a.csv',array2d,delimiter=',',newline='\n')
array = np.loadtxt('a.csv',delimiter=',')
print(array)



