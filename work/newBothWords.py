# -*- coding: utf-8 -*-
# Author: cong
# Copyrigh 2017
# 求出paper中共现的词语的数目存成 i j number(i,j共有的词语)
# 第一次处理，按年份，每个处理；

import numpy as py

import time
def main(file_list):
    for file in file_list:
        paper_dic = {}
        file_read = open(r"F:\classify_data\newMaterials\title_fos\title_fos"+ str(file) +".txt", 'r', encoding='utf-8')
        file_write = open(r"F:\classify_data\newMaterials\title_fos\title_fos"+ str(file) +"_both_words_result.txt", 'w',
                          encoding='utf-8')
        file_write2 = open(r"F:\classify_data\newMaterials\title_fos\title_fos"+ str(file) +"_words.txt", 'w',
                           encoding='utf-8')
        read_lines = file_read.readlines()
        count_select = 0
        for line in read_lines:
            count_select += 1
            if count_select % 3 == 0:
                line_list = line.split(",")
                line_key = line_list[0]
                line_value = line_list[1].rstrip()
                paper_dic[line_key] = line_value
            else:
                continue
        print("finish save to dic : " + str(time.time() - start_time))
        file_i = 0 # 文件标记
        count = 0 # 写文件计数
        count_num = 0 # 计算计数
        count_100 = 0
        count_2 = 0
        temp_str = ""
        print("len of keys: " + str(len(paper_dic.keys())))
        for key_i in paper_dic.keys():
            both_words_list = []
            for key_j in paper_dic.keys():
                if int(key_i) < int(key_j):
                    count_2 += 1
                    string_write = ""
                    value_i = paper_dic[key_i]
                    value_i_words = value_i.split(" ")
                    value_j = paper_dic[key_j]
                    value_j_words = value_j.split(" ")
                    both_have = set(value_i_words) & set(value_j_words)
                    both_words_list.extend(both_have)
                    len_both_have = len(both_have)
                    if len_both_have < 4:
                        continue
                    count_num += 1
                    count += 1 # 写文件计数
                    len_both_have = len_both_have - 3  # 同时减去9
                    string_write = key_i + " " + key_j + " " + str(len_both_have) + "\n"
                    temp_str += string_write
                    if count_num // 100 == 1:
                        count_num = count_num - 100
                        file_write.write(temp_str)
                        temp_str = ""
                        # print("写入了 1 万数据：" + str(time.time() - start_time))
                    if count // 30000000 == 1:
                        count = count - 30000000
                        file_i += 1
                        file_write.close()
                        file_write = open(r"F:\classify_data\newMaterials\title_fos\title_fos"+ str(file) +"_both_words_result" + str(
                            file_i) + ".txt", 'w', encoding='utf-8')
                    if count_2 // 5000000 == 1:
                        count_2 = count_2 - 5000000
                        count_100 += 1
                        print(str(count_100) + "个" + "500万条数据cost time：" + str(time.time() - start_time))
                else:
                    continue
            # print("count 计数 :" + str(count))
            for word in set(both_words_list):
                file_write2.write(word + "\n")
        file_write.close()
        file_write2.close()
        print("finish file " + str(file) +" : " + str(time.time() - start_time))
if __name__ == '__main__':
    start_time = time.time()
    file_list = ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17"]
    # file_list = ["12", "13", "14", "15", "16", "17"]
    main(file_list)
    print("finish write cost time : " + str(time.time() - start_time))