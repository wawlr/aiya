# -*- coding: utf-8 -*-
"""
@Time:2018/10/5 14:49
@Author:wangcong
一想到有那么多痴心姑娘等我，我的良心便有些痛。
"""
import time
import os
import json
import nltk
from gensim.corpora import Dictionary
from gensim.corpora import MmCorpus
from gensim.models import TfidfModel
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
# 读入数据 获取核心的词语（名次、动词类） 打上类别标签。处理好原始的数据集
# 处理后的原始数据的格式：ID，doi，文本信息（title和fos放在一起高权重，摘要放在一起低权重，这个地方权重可调节比较好），标签

# 调用聚类算法、网络算法处理数据集。参数需可调。

# 输出可比较的结果，对比证明算法的可行性。


def dealData():
    # 写文件
    path_write = "F:\\Data\\mixture\\paper_mixture.json"
    write_lines = open(path_write, 'w', encoding='utf-8')

    paper_file_path = "F:\\Data\\data"
    file_list = os.listdir(paper_file_path)
    count = 0
    for file in file_list:
        print(paper_file_path + "\\"+ file)
        # print(file[:-5])
        # paper.keys() 'doi', 'abstractUrl', 'Reference', 'Author', 'Abstract', 'Title', 'Cite', 'Volume', 'fullUrl', 'PublisherOrConference', 'AuthorInfo', 'Time', 'Keywords', 'Issue', 'Pages'
        # ID,doi,Title,Keywords,Abstract,Label
        for file_line in open(paper_file_path + "\\"+ file,'r',encoding='utf-8'):
            # print(file_line)

            if (file_line == "[\n") or (file_line == "]"):
                continue
            else:
                line = file_line.replace("},", "}")
                line2 = json.loads(line)
                # 打上标签
                line2['Label'] = file[:-5]
                line2['ID'] = str(count)
                # 处理分词完毕再形成paper_dic
                return_paper_json_dic = deal_nlp_dic(line2)
                json_info = json.dumps(return_paper_json_dic, sort_keys=True)
                write_lines.write(json_info+"\n")
                count += 1
    write_lines.close()




def deal_nlp_dic(paper_json_dic):
    return_paper_json_dic = {}
    return_paper_json_dic['doi'] = paper_json_dic['doi']
    return_paper_json_dic['Title'] = cut_sentence(paper_json_dic['Title'])
    return_paper_json_dic['Abstract'] = cut_sentence(paper_json_dic['Abstract'])
    # print("Keywords: "+str(paper_json_dic['Keywords']))
    #### Keywords中间词用• 分隔开  .replace("• ","")
    return_paper_json_dic['Keywords'] = " ".join(paper_json_dic['Keywords'])
    # print("Keywords: " + str(return_paper_json_dic['Keywords']))
    # print("Label: " + str(paper_json_dic['Label']))
    return_paper_json_dic['Label'] = paper_json_dic['Label']
    return_paper_json_dic['ID'] = paper_json_dic['ID']
    return return_paper_json_dic


def deal_nlp(paper_json_dic):
    ### 拿到json信息之后，处理成文本信息
    path_read = "F:\\Data\\paper_mixture.json"
    for line in open(path_read,'r',encoding='utf-8'):
        doi = line['doi']
        Title = line['Title']
        Abstract = line['Abstract']
        Keywords = line['Keywords']
        Label = line['Label']

    # 分词,取实体词处理

    # 计算词共现，保存到文件中。


# 分词，取实体词（动词、名词）
def cut_sentence(sentence):
    # 保留词性NNVB = ['CD','EX','FW','LS','NN','NNS','NNP','NNPS','PDT','POS','RP','VB','VBD','VBG','VBN','VBP','VBZ']
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem.lancaster import LancasterStemmer
    NNVB = ['CD', 'EX', 'FW', 'LS', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'RP', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
            'VBZ']
    # print("start:")
    texts_lower = [word for word in sentence.lower().split()]
    # print(texts_lower)
    texts_tokenized2 = [word.lower() for word in word_tokenize(sentence)]
    texts_tokenized2 = nltk.pos_tag(texts_tokenized2)
    texts_tokenized = []
    for item in texts_tokenized2:
        if item[1] in NNVB:
            texts_tokenized.append(item[0])
        else:
            continue
    # print(texts_tokenized)
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords = [word for word in texts_tokenized if not word in english_stopwords]
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_filtered = [word for word in texts_filtered_stopwords if not word in english_punctuations]
    # st = LancasterStemmer()
    # texts_stemmed = [st.stem(word) for word in texts_filtered]
    texts_filtered_str = " ".join(texts_filtered)
    # print(texts_filtered_str)
    return texts_filtered_str

# 处理tfidf，减小title和abstract的词语数目，更具有每篇文章的特征
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
        title_list = paper_json_data['Title']
        abstract_list = paper_json_data['Abstract']
        # print(abstract_list)
        paper_words = paper_json_data['Title']+" "+paper_json_data['Abstract']
        corpus_orgin.append(paper_words)
    # 对title和abstract进行 tfidf 训练
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus_orgin))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    # 输出非零元素对应的行坐标和列坐标
    nonzero = tfidf.nonzero() # m = nonzero[0][i]是代表第m篇文章，n = nonzero[1][p]是代表词袋模型第n个词
    return_list = get_tfidf_words(tfidf,word,return_words_number)

    # 写数据
    # 存数据入论文字典里
    print("write file: ")
    path_write = "F:\\Data\\mixture\\mixpaper_tfidf_words.json"
    write_lines = open(path_write, 'w', encoding='utf-8')
    tfidf_dic = {}
    for i in range(len(return_list)):
        tfidf_dic[i] = return_list[i]
    for id in papers_dic.keys():
        paper_json = papers_dic[id]
        paper_json["tfidf"] = return_list[id]
        # paper_json["tfidf"] = ",".join(return_list[id])
        json_info = json.dumps(paper_json, sort_keys=True)
        write_lines.write(json_info + "\n")
    write_lines.close()


def write_tfidf_words():
    paper_dic = {}
    return paper_dic

def get_tfidf_words(tfidf,word,return_words_number):
    nonzero = tfidf.nonzero() # m = nonzero[0][i]是代表第m篇文章，n = nonzero[1][p]是代表词袋模型第n个词
    k = 0  # k用来记录是不是一条记录结束了
    a_dic = {}
    words_return = []
    gather = []
    p = -1  # p用来计数，每走一遍循环+1
    for i in nonzero[0]:  # i不一定每循环就+1的，它是nonzero【0】里的数，不懂可以看之前输出的nonzero【0】
        p = p + 1
        # print(i, nonzero[1][p])
        if k == i:
            a_dic[word[nonzero[1][p]]] = tfidf[i, nonzero[1][p]]
        else:
            a_dic = sorted(a_dic.items(), key=lambda x: x[1], reverse=True)  # 对字典对象的排序
            # 返回的特征词数目
            words_return = []
            if len(a_dic) < return_words_number:
                return_words_number = len(a_dic)
            for iter_i in range(return_words_number):
                words_return.append(a_dic[iter_i][0])
            # print("a_dic: " + str(a_dic))
            # print("words_return: " + str(words_return))
            gather.append(words_return)
            while k < i:
                k = k + 1
            a_dic = {}
            # print("a[word[p]] = tfidf[i, nonzero[1][p]]："+str(word[p])+"  ")
            a_dic[word[nonzero[1][p]]] = tfidf[i, nonzero[1][p]]
    # print("words_return: " + str(words_return))
    gather.append(words_return)
    # print(gather)
    return gather

# 输入语料
def test_tfidf(corpus):
    id2word = {}
    corpus = MmCorpus("F:\\Data\\mixture\\model\\corpuse.mm")
    dictionary = Dictionary.load("F:\\Data\\mixture\\model\\dict")
    tfidfModel = TfidfModel.load("F:\\Data\\mixture\\model\\tfidf.model")
    corpus_tfidf = tfidfModel[corpus]
    return corpus_tfidf

## abstract中英文太多了，所以打算IFIDF处理。取出小于20个左右吧。
def dealSim():
    # 建立论文的字典，key是ID，value是paper的json转成的dic
    papers_dic = {}
    id_count = 0
    # 存数据入论文字典里
    path_read = "F:\\Data\\mixture\\paper_mixture.json"
    read_lines = open(path_read, 'r', encoding='utf-8')
    for line in read_lines:
        # print(line)
        json_data = json.loads(line)
        papers_dic[id_count] = json_data
        id_count += 1
    read_lines.close()
    # 计算相似度（词共现情况）,并保存下来
    path_write = "F:\\Data\\mixture\\paper_mixture_simmilarity.txt"
    write_lines = open(path_write, 'w', encoding='utf-8')
    write_sim = ""
    write_count = 0
    for paper_i in papers_dic.keys():
        for paper_j in papers_dic.keys():
            if paper_i < paper_j:
                write_count += 1
                # 一千次写一次
                if write_count % 1000 == 0:
                    write_lines.write(write_sim)
                    write_sim = ""
                # 计数计时
                if write_count %100000 ==0:
                    print("write count number: "+str(write_count)+"\n"+"cost time: "+str(time.time()-start_time))
                sum_words =sum_word_number(papers_dic[paper_i],papers_dic[paper_j],2,1,2)
                if sum_words >0:
                    write_sim += str(paper_i)+" "+str(paper_j)+" "+str(sum_words)+"\n"
    write_lines.write(write_sim)
    write_lines.close()

# 计算共现词语数目,输入是paper_dic
def sum_word_number(paper_dic1,paper_dic2,w_title=3,w_abstract=2,w_keywords=1):
    if paper_dic1['doi'] == paper_dic2['doi']:
        return -1
    else:
        w_title_scores = w_title * len(set(paper_dic1['Title'].split(" "))&set(paper_dic2['Title'].split(" ")))
        w_abstract_scores = w_abstract * len(set(paper_dic1['Abstract'].split(" "))&set(paper_dic2['Abstract'].split(" ")))
        w_keywords_scores = w_keywords * len(set(paper_dic1['Keywords'].split("• "))&set(paper_dic2['Keywords'].split("• ")))
        # print(paper_dic1['Keywords'].split("• "),paper_dic2['Keywords'].split("• "))
        sum_w  = w_title_scores + w_abstract_scores + w_keywords_scores
        # print(sum_w)
        return sum_w

if __name__ == '__main__':
    start_time = time.time
    # nltk.download()
    # dealData()
    # dealSim()
    train_tfidf(10)
