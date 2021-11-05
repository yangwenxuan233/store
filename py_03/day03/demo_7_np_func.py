import numpy as np

# 常用的函数 exp
def sigmoid(x):
    return 1/(1+np.exp((-x)))


print(np.exp(1))
print(np.exp([1,2,3,4,5,6,7,8,9,10]))

arr1 = np.array([1,2,3,4])
arr2 = np.array([11,12,13,14])
print(arr1 + arr2)

print(np.add(arr1,arr2))
arr3 = np.random.uniform(0,2,size=(4,5))   # 生成浮点数
arr4 = np.random.randint(1,10,size=(4,5))  # 生成整数
print(arr3)
print(arr4)

# python一个函数可以返回多值，如果没有返回值则默认返回None
y1,y2 = np.modf(arr3)   # y1存的小数 y2存的整数
print(y1,y2)

def sum1(x,y):
    return x,y,x+y,x-y,x/y

arr = sum1(10,20)
print(arr)
y1,y2,y3,y4,y5 = sum1(10,20)

print(np.power(2,10))  # 2**10
print(np.power([1,2,3,4],10))
print(np.array([1,2,3,4])**10)

# meshgrid
array = np.array([1,2,3])
xs,ys = np.meshgrid(array,array)
print(xs)
print(ys)

# np.where
array = np.array([10,50,100,90,80,70,55])
print(np.where(array >= 90,'优秀','一般'))
print(np.where(array >= 90,'优秀',array))
print(np.where(array >= 90,'优秀',np.where(array >= 80,'良好',np.where(array >= 70,'一般','其他'))))

print(np.sum(array))
print(np.mean(array))
print(np.std(array))   # 标准差
print(np.var(array))   # 方差

array2D = np.arange(1,11).reshape(2,5)
print(array2D)
print(np.mean(array2D,axis=0))  # 按行方向求
print(np.mean(array2D,axis=1))  # 按列方向求

# 分类问题
array = np.array([1,2,2,3,4,5,100,1000])
print(np.argmax(array))  # 返回最大值的下标
print(np.argmin(array))  # 返回最小值的下标

print((array > 5).sum())  # 布尔数组的求和

# sort
array.sort()
print(array)
print(np.unique(array))


