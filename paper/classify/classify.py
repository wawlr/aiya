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
    # 写文件
    path_write = "F:\\Data\\mixture\\paper_mixture.json"
    write_lines = open(path_write, 'w', encoding='utf-8')

    paper_file_path = "F:\\Data\\data"
    file_list = os.listdir(paper_file_path)
    for file in file_list:
        print(paper_file_path + "\\"+ file)
        # print(file[:-5])
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
                # 打上标签
                line2['Label'] = file[:-5]
                # 处理分词完毕再形成paper_dic
                return_paper_json_dic = deal_nlp_dic(line2)
                json_info = json.dumps(return_paper_json_dic, sort_keys=True)
                write_lines.write(json_info+"\n")
                # print("JSON输出：")
                # print(type(json_info))
                # print(json_info)
                # texts_stemmed = cut_sentence(line2['Title'])
                # print(texts_stemmed)

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

# 计算共现词语数目,输入是dic
def sum_word_number(paper_dic1,paper_dic2,p1,p2,p3):
    paper_dic1

    both_have = set(list_1) & set(list_2)
    len_both_have = len(both_have)
    return len_both_have





if __name__ == '__main__':
    start_time = time.time
    # nltk.download()
    dealData()
