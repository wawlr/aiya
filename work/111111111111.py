# -*- coding: utf-8 -*-
"""
@Time:2018/10/11 19:05
@Author:wangcong
一想到有那么多痴心姑娘等我，我的良心便有些痛。
"""
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
# 读入数据 获取核心的词语（名次、动词类） 打上类别标签。处理好原始的数据集
# 处理后的原始数据的格式：ID，doi，文本信息（title和fos放在一起高权重，摘要放在一起低权重，这个地方权重可调节比较好），标签

# 调用聚类算法、网络算法处理数据集。参数需可调。

# 输出可比较的结果，对比证明算法的可行性。


def dealData():
    paper_file_path = "F:\\Data\\data"
    file_list = os.listdir(paper_file_path)
    for file in file_list:
        print(paper_file_path + "\\"+ file)
        print(file[:-5])
        count = 0
        # paper.keys() 'doi', 'abstractUrl', 'Reference', 'Author', 'Abstract', 'Title', 'Cite', 'Volume', 'fullUrl', 'PublisherOrConference', 'AuthorInfo', 'Time', 'Keywords', 'Issue', 'Pages'
        # ID,doi,Title,Keywords,Abstract,Label
        for file_line in open(paper_file_path + "\\"+ file,'r',encoding='utf-8'):
            # print(file_line)
            count += 1
            if (file_line == "[\n") or (file_line == "]"):
                continue
            else:
                line = file_line.replace("},", "}")
                line2 = json.loads(line)
                # print(line2)

def deal_nlp(paper_json_dic):
    ### 拿到json信息之后，处理成文本信息
    path_read = "F:\\Data\\data\\paper_mixture.json"
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
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem.lancaster import LancasterStemmer
    texts_lower = [word for word in sentence.lower().split()]
    texts_tokenized = [word.lower() for word in word_tokenize(sentence.decode('utf-8'))]
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords = [word for word in texts_tokenized if not word in english_stopwords]
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_filtered = [word for word in texts_filtered_stopwords if not word in english_punctuations]
    st = LancasterStemmer()
    texts_stemmed = [st.stem(word) for word in texts_filtered]
    return texts_stemmed

# 计算共现词语数目
def sum_word_number(list_1,list_2):
    both_have = set(list_1) & set(list_2)
    len_both_have = len(both_have)
    return len_both_have





if __name__ == '__main__':
    start_time = time.time
    nltk.download()
    dealData()
