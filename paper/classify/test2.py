# -*- coding: utf-8 -*-
"""
@Time:2018/10/20 11:24
@Author:wangcong
一想到有那么多痴心姑娘等我，我的良心便有些痛。
"""
from gensim.corpora import Dictionary
from gensim.corpora import MmCorpus
from gensim.models import TfidfModel
import json
def train_tfidf(return_words_number = 20):
    # 建立论文的字典，key是ID，value是paper的json转成的dic
    papers_dic = {}
    id_count = 0
    # 存数据入论文字典里
    path_read = "F:\\Data\\mixture\\paper_mixture.json"
    read_lines = open(path_read, 'r', encoding='utf-8')
    for line in read_lines:
        # print(line)
        json_data = json.loads(line)
        # json_data[str(id_count)] = json_data
        papers_dic[id_count] = json_data
        id_count += 1
    read_lines.close()
    # 生成语料 corpus_orgin
    corpus_orgin = []
    for id in range(id_count):
        paper_json_data = papers_dic[id]
        title_list = paper_json_data['Title'].split(" ")
        abstract_list = paper_json_data['Abstract'].split(" ")
        # print(abstract_list)
        paper_words = title_list
        paper_words.extend(abstract_list)
        corpus_orgin.append(paper_words)
    # 对title和abstract进行 tfidf 训练
    id2word = {}
    # 生成并保存字典
    dictionary = Dictionary(corpus_orgin)
    dictionary.save("F:\\Data\\mixture\\model\\dict")
    # 将文档转换成词袋(bag of words)模型
    corpus = [dictionary.doc2bow(text) for text in corpus_orgin]
    # 保存生成的语料
    MmCorpus.serialize('F:\\Data\\mixture\\model\\corpuse.mm', corpus)
    del corpus_orgin
    # 训练模型
    tfidfModel = TfidfModel(corpus=corpus, id2word=id2word, dictionary=dictionary)
    tfidfModel.save("F:\\Data\\mixture\\model\\tfidf.model")
    corpus_tfidf = tfidfModel[corpus]


# 输入语料
def test_tfidf(corpus):
    id2word = {}
    corpus = MmCorpus("F:\\Data\\mixture\\model\\corpuse.mm")
    dictionary = Dictionary.load("F:\\Data\\mixture\\model\\dict")
    tfidfModel = TfidfModel.load("F:\\Data\\mixture\\model\\tfidf.model")
    corpus_tfidf = tfidfModel[corpus]
    return corpus_tfidf

