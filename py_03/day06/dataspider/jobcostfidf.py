from dataspider.dao.jobdao import JobDao
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import jieba
import numpy as np

texts = []

jobDao=JobDao()

data=jobDao.getAllJobInfo()

for row in data:
    texts.append(' '.join(jieba.cut(row['job_info'])))
    pass

# TF = 2/5 = 0.4   IDF = log(11/(3)） = 1.29   TF-IDF('人工智能') = 0.33 * 1.29 = 0.52
# jieba

vectorizer  = CountVectorizer()

# 传入词库，用于统计词库和词数
tf = vectorizer.fit_transform(texts)

# 得到词库。词汇表
words = vectorizer.get_feature_names()
print(words)

# 查看词频统计
print(tf.toarray()) #

tfidfTransformer = TfidfTransformer()

# 计算tf-idf
tfiwf = tfidfTransformer.fit_transform(tf)
# 查看每句话的tf-idf值
print(tfiwf.toarray())

from sklearn.metrics.pairwise import linear_kernel


# 通过向量的余弦相似度，计算出第一个文本和所有其他文本之间的相似度（注意此处包含了自己）
cosine_similarities = linear_kernel(tfiwf[0:1], tfiwf[1:]).flatten()
print(cosine_similarities)
print(np.argmax(cosine_similarities))

#[1.         0.21301212 0.19262788 0.37327551]
#从结果来看，第一条数据和自己的相似度是1，完全相似，和第4条文本相似度最高是37%的相似度，实际也是如此。
