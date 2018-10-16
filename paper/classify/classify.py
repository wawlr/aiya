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

def dealSim():
    # 建立论文的字典，key是ID，value是paper的json转成的dic
    papers_dic = {}
    id_count = 0
    # 存数据入论文字典里
    path_read = "F:\\Data\\mixture\\paper_mixture.json"
    read_lines = open(path_read, 'r', encoding='utf-8')
    for line in read_lines:
        json_data = json.load(line)
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

                sum_words =sum_word_number(papers_dic[paper_i],papers_dic[paper_j],2,1,2)
                if sum_words >0:
                    write_sim += str(paper_i)+" "+str(paper_j)+" "+str(sum_words)+"\n"
    write_lines.write(write_sim)
    write_lines.close()

# 计算共现词语数目,输入是paper_dic
def sum_word_number(paper_dic1,paper_dic2,w_title=2,w_abstract=1,w_keywords=2):
    if paper_dic1['doi'] == paper_dic2['doi']:
        return -1
    else:
        w_title_scores = w_title * len(set(paper_dic1['Title'].split(" "))&set(paper_dic2['Title'].split(" ")))
        w_abstract_scores = w_abstract * len(set(paper_dic1['Abstract'].split(" "))&set(paper_dic2['Abstract'].split(" ")))
        w_keywords_scores = w_keywords * len(set(paper_dic1['Keywords'].replace("•",""))&set(paper_dic2['Keywords'].replace("•","")))
        return sum(w_title_scores+w_abstract_scores+w_keywords_scores)

if __name__ == '__main__':
    start_time = time.time
    # nltk.download()
    dealData()
    dealSim()
