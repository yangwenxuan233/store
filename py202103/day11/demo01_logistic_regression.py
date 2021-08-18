import numpy as np

# 定义激活函数
def sigmoid(x):
    return 1/(1 + np.exp(-x))
    pass

# 预测函数
def predict(X,w):
    return sigmoid(X.dot(w))
    pass
# 定义loss
def loss(X,w,y):
    py = predict(X,w)
    logpy = np.array([0 if p == 0 else np.log(p) for p in py])
    logpy1 = np.array([0 if 1-p == 0 else np.log(1-p) for p in py])
    return np.sum(-y * logpy-(1-y)*logpy1)/len(X)
    pass

def gradient(X,w,y):
    return X.T.dot(predict(X,w)-y)/len(X)
    pass

def train(X,w,y,alpha=0.001,rat=0.00001,times=10000):
    loss_0 = loss(X,w,y)
    g_w = gradient(X,w,y)
    w1 = w - alpha*g_w
    loss_1 = loss(X,w1,y)
    t = 1
    while np.abs(loss_1 - loss_0) > rat:
        loss_0 = loss_1
        w = w1
        g_w= gradient(X,w,y)
        w1 = w-alpha*g_w
        loss_1 = loss(X,w1,y)
        t +=1
        if t > times:
            break
            pass
        pass
    return w
    pass
trainX = np.array([[1,50,89],
                   [1,40,40],
                   [1,60,70],
                   [1,50,40],
                   [1,80,80],
                   [1,90,80],
                   [1,66,60],
                   [1,50,80],
                   [1,80,50],
                   [1,20,10]])
trainY = np.array([0,0,1,0,1,1,1,0,0,0])
#
trainX = trainX/100

