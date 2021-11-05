import numpy as np
# 构造训练样本
trainX = [['你','是','一个','好人','好人','有','好报'],
          ['你','是','一头','猪'],
          ['你','吃了','吗'],
          ['你','是','一个','聪明','的','人'],
          ['你','是','一个','坏人'],
          ['打','球','去'],
          ['你','是','真','帅']]
trainY = [0,1,2,0,1,2,0]

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
    py0 = 4/8
    py1 = 2/8
    py2 = 2/8
    # 概率值就是预测模型
    xy0 = np.zeros(len(vvList))
    xy1 = np.zeros(len(vvList))
    xy2 = np.zeros(len(vvList))
    for x,y in zip(trainArray,trainY):
        if y == 0:
            xy0 += x
            pass
        elif y == 1:
            xy1 += x
            pass
        else:
            xy2 += x
            pass
        pass
    print(xy0)
    print(xy1)
    print(xy2)
    totalxy0 = np.sum(xy0)
    totalxy1 = np.sum(xy1)
    totalxy2 = np.sum(xy2)
    print(totalxy0)  # y=0的句子总词数
    print(totalxy1)  # y=1的句子总词数
    print(totalxy2)  # y=2的句子总词数
    pxy0 = (xy0 + 1)/(totalxy0 + len(vvList))   # 平滑处理
    pxy1 = (xy1 + 1)/(totalxy1 + len(vvList))
    pxy2 = (xy2 + 1)/(totalxy2 + len(vvList))
    return py0,py1,py2,pxy0,pxy1,pxy2
    pass
# 模型参数
py0,py1,py2,pxy0,pxy1,pxy2 = bayers(trainArray,trainY,vvList)
# 预测
def predict(data,py0,py1,py2,pxy0,pxy1,pxy2):
    p0 = np.sum(data[0] * np.log(pxy0)) + np.log(py0)
    p1 = np.sum(data[0] * np.log(pxy1)) + np.log(py1)
    p2 = np.sum(data[0] * np.log(pxy2)) + np.log(py2)
    array = np.array([p0,p1,p2])
    p = np.max(array)
    if p0 == p:
        return 0
        pass
    elif p1 == p:
        return 1
        pass
    else:
        return 2
        pass
    pass
data = [['你','坏人']]
textX = makeTrainX(data,vvList)
print(textX)
result = predict(textX,py0,py1,py2,pxy0,pxy1,pxy2)
print(result)
