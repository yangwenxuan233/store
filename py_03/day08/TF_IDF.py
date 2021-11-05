#!/usr/bin/env python
# coding: utf-8

# ## 演练4002：TF-IDF特征处理
# 
# 案例1：利用词频(TF)和逆文本频率指数(IDF)，计算出字或词在文档中的重要性，使用scikit-learn包实现。
# 步骤包括：文本语料获取、词频矩阵转换、TF-IDF计算

# ### 前置步骤：安装scikit-learn
# pip install -U sklearn

# ### TF-IDF原理：
# TF-IDF（Term Frequency-InversDocument Frequency）是一种常用于信息处理和数据挖掘的加权技术。该技术采用一种统计方法，根据字词在文本中出现的次数和在整个语料文档中出现的频率来计算一个字词在整个语料中的重要程度。它的优点是能过滤掉一些常见的却无关紧要本的词语，同时保留影响整个文本的重要字词。
# 
# TF（Term Frequency）表示某个关键词在整个文本中出现的频率。
# IDF（InversDocument Frequency）表示计算倒文本频率。文本频率是指某个关键词在整个语料所有文章中出现的次数。倒文档频率又称为逆文档频率，它是文档频率的倒数，主要用于降低所有文档中一些常见却对文档影响不大的词语的作用。
# 
# ### 案例1：
# 假设有一个语料库由1000篇文章组成，总共的词汇数为5000个，也就是总共有5000个不同的词。
# 现在有一篇文章总共有10000个词（词可以重复），2000个词汇，其中“学习”这个词出现了100次，“人工智能”这个词出现了200次，“自然”出现了150次，“语言”出现了300次。
# 假设在这1000篇文章中，出现过“学习”的文章数为99篇，出现过“人工智能”的文章数位199篇，出现过“自然”的文章数为49篇，出现过“语言”的文章数位999篇。
# 
# ###  步骤1：计算词频
# TF(学习)=100/10000=0.01
# TF(人工智能)=200/10000=0.02
# TF(自然)=150/10000=0.015
# TF(语言)=300/10000=0.03
# 
# ### 步骤2：计算IDF
# log以10为底计算IDF：
# IDF(学习)=log(1000/100)=1
# IDF(人工智能)=log(1000/200)=0.698
# IDF(自然)=log(1000/50)=1.30
# IDF(语言)=log(1000/1000)=0
# 计算结果可以看出词语出现过的文章数越多，则IDF值越小，说明这个词很可能是“是”，“的”，“吗”等
# 
# ### 步骤3：计算TF-IDF：
# TF-IDF(学习)=0.01*1=0.01
# TF-IDF(人工智能)=0.02*0.698=0.014
# TF-IDF(自然)=0.015*1.30=0.019
# TF-IDF(语言)=0.03*0 = 0
# 
# ### 步骤4：代码实现
# sklearn算法改进的传统的TF-IDF算法 改进TF-IWF

# In[13]:


from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

texts = ['人工智能 学习 自然 语言 喜欢 人工智能',
         '我 喜欢 吃鸡',
         '人工智能 是 未来 的 重点 学科',
         '我 爱 人工智能 还是 人工智能 好啊']

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
cosine_similarities = linear_kernel(tfiwf[0:1], tfiwf).flatten()
print(cosine_similarities)

# [1.         0.21301212 0.19262788 0.37327551]
# 从结果来看，第一条数据和自己的相似度是1，完全相似，和第4条文本相似度最高是37%的相似度，实际也是如此。