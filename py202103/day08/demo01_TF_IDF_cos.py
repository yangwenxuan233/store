import numpy as np
import jieba
texts=['人工智能学习自然语言喜欢人工智能',
       '我喜欢吃鸡',
       '人工智能是未来学科重点',
       '我喜欢人工智能还是人工智能好啊学习',
       '我爱学习',
        '吃吃']


def countVectorizer(texts):
    vectorizer=[]
    vSet=set()
    listW=[]
    for text in texts:
        row=list(jieba.cut(text))
        listW.append(row)
        vSet=vSet|set(row)
        pass
    vectorizer=list(vSet)
    print(vectorizer)
    #根据词典统计词频
    #wordTimes=np.zeros(vectorizer)
    listCount=[]
    for row in listW:
        rowCount=np.zeros(len(vectorizer))
        for word in row:
            index=vectorizer.index(word)
            rowCount[index]+=1
            pass
        listCount.append(rowCount)
        pass
    return vectorizer,np.array(listCount)
    pass
vectorizer,listCount=countVectorizer(texts)
print(listCount)
def tfidf(vectorizer,listCount):
    tf=np.array([row/np.sum(row) for row in listCount])
    idf=np.array([np.log10(len(listCount)/(np.count_nonzero(row)+1)) for row in listCount.T])
    print(tf)
    print(idf)
    tfIDF=tf*idf
    print(tfIDF)
    return tfIDF
    pass
tfIDF=tfidf(vectorizer,listCount)
def cos(row,tfIDF):
    listCos=[]
    for r in tfIDF:
        cc=np.sum(r*row)/((np.sum(r**2)**0.5)*(np.sum(row**2)**0.5))
        listCos.append(cc)
        pass
    return listCos
    pass
print(cos(tfIDF[0],tfIDF))
