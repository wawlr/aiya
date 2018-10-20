#
# # -*- coding: utf-8 -*-
# """
# @Time:2018/10/19 16:42
# @Author:wangcong
# 一想到有那么多痴心姑娘等我，我的良心便有些痛。
# """
#
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
#
# corpus = ["I come to China to travel",
#           "This is a car polupar in China",
#           "I love tea and Apple ",
#           "The work is to write some papers in science"]
#
# vectorizer = CountVectorizer()
#
# transformer = TfidfTransformer()
# tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
#
# # print(tfidf)
#
# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf2 = TfidfVectorizer()
# re = tfidf2.fit_transform(corpus)
# print(re)

# coding:utf-8
__author__ = "liuxuejiang"
# import jieba
# import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == "__main__":
    corpus = ["我 来到 北京 清华大学",  # 第一类文本切词后的结果，词之间以空格隔开
              "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果
              "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
              "我 爱 北京 天安门"]  # 第四类文本的切词结果
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    print(word)
    print(type(tfidf))
    print(tfidf)
    # 输出非零元素对应的行坐标和列坐标
    nonzero = tfidf.nonzero()
    # nonzero是个tuple
    print(type(nonzero))
    # print(nonzero[0])
    # print(nonzero[1])

    k = 0  # k用来记录是不是一条记录结束了
    a_dic = {}
    gather = []
    p = -1  # p用来计数，每走一遍循环+1
    for i in nonzero[0]:  # i不一定每循环就+1的，它是nonzero【0】里的数，不懂可以看之前输出的nonzero【0】
        p = p + 1
        print(i, nonzero[1][p])
        if k == i:
            a_dic[word[nonzero[1][p]]] = tfidf[i,nonzero[1][p]]
        else:
            a_dic = sorted(a_dic.items(), key=lambda x: x[1], reverse=True)  # 对字典对象的排序
            print("a_dic: "+ str(a_dic))
            gather.append(a_dic)
            while k < i:
                k = k + 1
            a_dic = {}
            # print("a[word[p]] = tfidf[i, nonzero[1][p]]："+str(word[p])+"  ")
            a_dic[word[nonzero[1][p]]] = tfidf[i, nonzero[1][p]]
    print(a_dic)
    gather.append(a_dic)
    print(gather)