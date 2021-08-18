import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# 损失函数  w=[w0,w1,w2...wn] X=[[1,x11,x12,x13...x1n],
#                               [1,x21,x22,x23...x2n]
#                               ...
#                               [1,xm1,xm2,xm3...xmn]]
def loss(X,y,w):
    return np.sum((X.dot(w)-y)**2)/2/len(X)
    pass

def gradient(X,y,w):
    return X.T.dot((X.dot(w)-y))
    pass

def train(X,y,w,alpha=0.001,rat=0.00001,times=10000):
    loss_0 = loss(X,y,w)
    g_w = gradient(X,y,w)
    w1 = w - alpha*g_w
    loss_1 = loss(X,y,w1)
    t = 1
    while np.abs(loss_1 - loss_0) > rat:
        loss_0 = loss_1
        w = w1
        g_w= gradient(X,y,w)
        w1 = w-alpha*g_w
        loss_1 = loss(X,y,w1)
        t +=1
        if t > times:
            break
            pass
        pass
    return w
    pass
def predict(X,y,w):
    y =  X.dot(w)
    return y
    pass

X = np.array([[1,6,2],
              [1,8,1],
              [1,10,0],
              [1,14,2],
              [1,18,0]])
y = np.array([7,9,13,17.5,18])

w = train(X,y,np.array([1,2,3]))
print(w)
print(predict(X,y,w))

xx1 = X[:,1]
xx2 = X[:,2]
xs , ys = np.meshgrid(xx1,xx2)
print(xs,ys)
sx = np.arange(0,20,0.1)
xss,yss = np.meshgrid(sx,sx)
print(xss)
print(yss)
z=[]
'''
for rowx,rowy in zip(xss,yss):
    zrow = []
    for x1,x2 in zip(rowx,rowy):
        zs = w[0] + x1*w[2] +x2*w[1]
        zrow.append(zs)
        pass
    z.append(zrow)
    pass
z = np.array(z)
'''
z = xss*w[1] + yss*w[2]+w[0]
fig = plt.figure()
ax = Axes3D(fig)

# 表面

ax.plot_surface(xss,yss,z,rstride=1,cstride=1)
ax.scatter3D(xx1,xx2,y)
plt.show()

# 做实验
def generateData(w,x):
    return w[0] + w[1] * (x[1]**2) + w[2]*(x[2]**2) + w[3] * x[1]
    pass

w = np.array([1,2,3])
x = np.array([[1,1,2],
              [1,2,2],
              [1,3,3],
              [1,2,2],
              [1,4,1]])
y = np.array([generateData(w,xx) for xx in x] + np.random.uniform(-1,1,size=(5,)))
print(y)

trainX = np.array([[1,1,4,1],
                   [1,4,4,2],
                   [1,9,9,3],
                   [1,4,4,2],
                   [1,16,1,4]])
neww = train(trainX,y,w=np.array([0.1,0.2,0.3,1]))
print(neww)

# 归一化 标准化
fig = plt.figure()
ax = Axes3D(fig)
sx = np.arange(0,20,0.1)
xss,yss = np.meshgrid(sx,sx)
z = neww[0] + neww[1]*xss**2 + neww[2]*yss**2 +neww[3]*xss

ax.plot_surface(xss,yss,z,rstride=1,cstride=1)
ax.scatter3D(x[:,1],x[:,2],y,c='r')
plt.show()





