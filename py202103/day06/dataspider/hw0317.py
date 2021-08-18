from dataspider.dao.jobdao import JobDao
import numpy as np
import jieba
texts=[]
jobDao=JobDao()

data=jobDao.getAllJobInfo()

for row in data:
    texts.append(' '.join(jieba.cut(row['job_info'])))
    pass

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
