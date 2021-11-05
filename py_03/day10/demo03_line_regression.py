import numpy as np
import matplotlib.pyplot as plt
# f(x)=w0+w1*x

def predict(x,w0,w1):
    return w0 + w1*x
    pass

def loss(x,y,w0,w1):
    return np.sum((y-predict(x,w0,w1))**2)/2/len(x)
    pass

def gradient(x,y,w0,w1):
    g_w0 = 2*np.sum((predict(x,w0,w1)-y))/len(x)
    g_w1 = 2*np.sum((predict(x,w0,w1)-y)*x)/len(x)
    return g_w0,g_w1
    pass
# 基于梯度下降算法
def train(x,y,w0,w1,alpha=0.001,rat=0.00001,times=10000):
    loss_0 = loss(x,y,w0,w1)
    g_w0,g_w1 = gradient(x,y,w0,w1)
    w0_1 = w0 - alpha*g_w0
    w1_1 = w1 - alpha*g_w1
    loss_1 = loss(x,y,w0_1,w1_1)
    t = 1
    while np.abs(loss_1 - loss_0) > rat:
        loss_0 = loss_1
        w0,w1 = w0_1,w1_1
        g_w0,g_w1 = gradient(x,y,w0,w1)
        w0_1 = w0-alpha*g_w0
        w1_1 = w1-alpha*g_w1
        loss_1 = loss(x,y,w0_1,w1_1)
        t +=1
        if t > times:
            break
            pass
        pass
    return w0,w1
    pass
x = np.array([4,6,8,10,12])
y = np.array([9,11.9,17,19,25])

w0,w1 = train(x,y,1,2)

py = predict(x,w0,w1)
plt.scatter(x,y,c='r')
plt.plot(x,py)
plt.show()
