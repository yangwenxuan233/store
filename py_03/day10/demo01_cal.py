import numpy as np
import matplotlib.pyplot as plt
# 损失函数（成本函数）
def loss(x):
    return x**2
    pass

def gradient(x):
    return 2*x
    pass

listX = []
# 数值迭代无限逼近
def train(x,alpha=0.01,times=100000,rat=0.00001):

    x_g = gradient(x)
    x1 = x-alpha*x_g
    t = 0
    while np.abs(loss(x)-loss(x1)) > rat:
        listX.append(x)
        x_g = gradient(x1)
        x = x1
        x1 = x-alpha*x_g
        t += 1
        if t > times:
            print('超出了迭代次数，无法收敛')
            break
            pass
        pass
    return x
    pass
r = train(10)
print(r)

y = loss(np.array(listX))
x = np.arange(-10,11,1)
plt.plot(x,loss(x))
plt.scatter(listX,y,c='r')
plt.show()