import numpy as np

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
    return X.dot(w)
    pass

X = np.array([[1,6,2],
              [1,8,1],
              [1,10,0],
              [1,14,2],
              [1,18,0]])
y = [7,9,13,17.5,18]

w = train(X,y,np.array([1,2,3]))
print(w)
print(predict(X,y,w))


