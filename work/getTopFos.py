# -*- coding: utf-8 -*-
# Author: cong
# Copyrigh 2017
# 统计分析出现的社团划分的同一个社团论文的数目，看看计算的阈值。
# 知道到每个社团出现的fos的词频
# 之前是阈值是50，现在改成30,测试的时候是10


import pandas as pd
import time

def main():
    start_time = time.time()
    file_read = open("F:\\classify_data\\newMaterials\\title_fos\\fos_title_every_year_data_both_exist_new_result.txt",
                       'r', encoding='utf-8')
    read_lines = file_read.readlines()
    file_read_fos = open(r"F:\classify_data\newMaterials\index_year_fos.txt",'r',encoding='utf-8')
    read_fos_lines = file_read_fos.readlines()
    index_fos_dic = save_fos_todic(read_fos_lines)
    file_write = open(r"F:\classify_data\newMaterials\title_fos\06_17_index_fos_result.txt",'w',encoding='utf-8')
    find_fos(read_lines,index_fos_dic,file_write)
    print(" finish find fos : "+ str(time.time() - start_time))
    # find fos
    file_read_fos = open(r"F:\classify_data\newMaterials\title_fos\06_17_index_fos_result.txt", 'r', encoding='utf-8')
    read_fos_lines = file_read_fos.readlines()
    file_write_fos = open(r"F:\classify_data\newMaterials\title_fos\06_17_index_fos_result_fos.txt", 'w', encoding='utf-8')
    get_top_fos(read_fos_lines,file_write_fos)
    print( " finish get top fos : " + str(time.time() - start_time) )
def find_fos(read_lines,index_fos_dic,file_write):
    for line in read_lines:
        line_list = line.split(" ")
        string_fos = ""
        # print(line_list)
        for i in range(len(line_list) - 1):
            index_number = line_list[i]
            index_number = str(index_number.rstrip())
            fos_string = index_fos_dic[index_number]
            # print(index_fos_dic[index_number])
            string_fos = string_fos + fos_string + ","
        string_fos = string_fos[:-1]
        string_fos += "\n"
        file_write.write(string_fos)
    file_write.close()

def get_top_fos(readlines,file_write_fos):
    for line in readlines:
        top_fos_dic = {}
        line_list = line.split(",")
        for words in line_list:
            words = words.lower()
            # print("words lower : " + str(words))
            if words in top_fos_dic.keys():
                top_fos_dic[words] = top_fos_dic[words] + 1
            else:
                top_fos_dic[words] = 1

        fos_dic = {}
        for key in top_fos_dic.keys():
            if top_fos_dic[key] > 20:
                fos_dic[key] = top_fos_dic[key]
        list_fos_key = [v for v in sorted(fos_dic.items(), key=lambda d: d[1],reverse=True)]
        fos_dic_sort = {}
        string_fos = ""
        for item in list_fos_key:
            fos_dic_sort[item[0]] = item[1]
            string_fos = string_fos + "," + str(item[0])
        string_fos = string_fos[1:] + "\n"
        file_write_fos.write(string_fos)
        # print("list_fos_key: ")
        # print(list_fos_key)
        # print(string_fos)
        # print(fos_dic)
        # print(top_fos_dic)
        list_fos = [v for v in sorted(top_fos_dic.values(),reverse = True)]
        # print(list_fos)

def save_fos_todic(read_lines):
    string_dic = {}
    for line in read_lines:
        line_list = line.split("$")
        line_fos = line_list[2].strip('\n')
        # print(line_fos)
        string_dic[str(line_list[0])] = line_fos
    # print(string_dic)
    return string_dic
if __name__ == '__main__':
    main()