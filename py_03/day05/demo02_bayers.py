import numpy as np

# 手写实现贝叶斯算法

# 构造训练样本
trainX = [['你','是','一个','好人','好人','有','好报'],
          ['你','是','一头','猪'],
          ['你','是','一个','聪明','的','人'],
          ['你','是','一个','坏人'],
          ['你','是','真','帅'],
          ['你','真','好人']]
trainY = [0,1,0,1,0,0]

# 构造词典
def vList(trainX):
    vSet = set()
    for x in trainX:
        vSet = vSet | set(x)
        pass
    return list(vSet)
pass
vvList = vList(trainX)
print(vvList)

# 训练数据中每个词出现的次数的计数作为训练数据,词频统计
def makeTrainX(trainX,vvList):
    listX = []
    for x in trainX:
        zArray = np.zeros(len(vvList))
        for w in x:
            index = vvList.index(w)
            zArray[index] += 1
            pass
        listX.append(zArray)
    pass
    return np.array(listX)
pass
trainArray = makeTrainX(trainX,vvList)
print(trainArray)   # 词频

def bayers(trainArray,trainY,vvList):
    py0 = 4/6
    py1 = 2/6
    # 概率值就是预测模型
    xy0 = np.zeros(len(vvList))
    xy1 = np.zeros(len(vvList))
    for x,y in zip(trainArray,trainY):
        if y == 0:
            xy0 += x
            pass
        else:
            xy1 += x
            pass
        pass
    print(xy0)
    print(xy1)
    totalxy0 = np.sum(xy0)
    totalxy1 = np.sum(xy1)
    print(totalxy0)  # y=0的句子总词数
    print(totalxy1)  # y=1的句子总词数
    pxy0 = (xy0 + 1)/(totalxy0 + len(vvList))   # 平滑处理
    pxy1 = (xy1 + 1)/(totalxy1 + len(vvList))
    return py0,py1,pxy0,pxy1
    pass
# 模型参数
py0,py1,pxy0,pxy1 = bayers(trainArray,trainY,vvList)

# 预测
def predict(data,py0,py1,pxy0,pxy1):
    p0 = np.sum(data[0] * np.log(pxy0)) + np.log(py0)
    p1 = np.sum(data[0] * np.log(pxy1)) + np.log(py1)
    if p0 > p1:
        return 0
        pass
    else:
        return 1
        pass
    pass
data = [['你','好人']]
textX = makeTrainX(data,vvList)
print(textX)
result = predict(textX,py0,py1,pxy0,pxy1)
print(result)


