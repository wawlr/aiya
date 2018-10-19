# -*- coding: utf-8 -*-
"""
@Time:2018/10/18 20:17
@Author:wangcong
一想到有那么多痴心姑娘等我，我的良心便有些痛。
"""
# 加载训练数据,去除停止词
from gensim.corpora import Dictionary
import gensim.corpora
def getCorpus():
    corpus_orgin = []
    count = 0
    corpus_list = []
    with open("D:wiki_cn\zh.jian.wiki.seg-1.3g", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(lines.__len__())
        for sentence in lines:
            words = sentence.split(" ")
            sentence_segment = []
            for word in words:
                if word.strip() != '':
                    if word.strip() not in stopwords:
                        sentence_segment.append(word.strip())
            corpus_list.append(sentence_segment)
            count += 1
            if count % 1000 == 0:
                logger.info("model train finished" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print("processd " + str(count) + " segment_sentence")
    return corpus_list
corpus_list = getCorpus()

id2word = {}
# 生成并保存字典
dictionary = Dictionary(corpus_list)
dictionary.save("./model/dict")
# 将文档转换成词袋(bag of words)模型
corpus = [dictionary.doc2bow(text) for text in corpus_list]
# 保存生成的语料
MmCorpus.serialize('./model/corpuse.mm', corpus)
del corpus_list
corpus_tfidf = []
def train():
    tfidfModel = TfidfModel(corpus=corpus, id2word=id2word, dictionary=dictionary)
    tfidfModel.save("./model/tfidf.model")
    corpus_tfidf = tfidfModel[corpus]
train()

