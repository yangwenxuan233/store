import numpy as np
import matplotlib.pyplot as plt
# f(x)=w0+w1*x

def predict(x,w0,w1):
    return w0 + w1*x
    pass

def loss(x,y,w0,w1):
    return np.sum((y-predict(x,w0,w1))**2)
    pass

def gradient(x,y,w0,w1):
    g_w0 = 2*np.sum((y-predict(x,w0,w1)))
    g_w1 = 2*np.sum((y-predict(x,w0,w1))*x)
    pass
# 基于方程组： 一阶导数的方程组
def train(x,y):
    w1 = np.cov(x,y)[0][1]/np.var(x)
    w0 = np.mean(y)-w1*np.mean(x)
    return w0,w1
    pass
x = np.array([4,6,8,10,12])
y = np.array([9,11.9,17,19,25])

w0,w1 = train(x,y)
print(w0,w1)
py = predict(x,w0,w1)
plt.scatter(x,y,c='r')
plt.plot(x,py)
plt.show()
print(predict(14,w0,w1))
