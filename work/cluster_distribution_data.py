# -*- coding: utf-8 -*-
# Author: cong
# Copyrigh 2017
### 统计社团的文章的数目，确定社团大小的阈值，选出大社团中的文章，得到对应的数据
### 取得每年的大于阈值的社团的论文id，写到文件中。

# 目的是找到每年的大于阈值的社团论文的id

import time
def calculate(line,file):
    global distribution
    if file not in distribution.keys():
        distribution[file] = line
    else:
        line_temp = distribution[file]
        line_temp = line_temp + str(file)+ "," + line
        distribution[file] = line_temp

def get_number(read_line):
    for line in read_line:
        line_list = line.split(" ")
        line_number = line_list[2].rstrip()
        calculate(line_number)

def write_distribution(distribution,file_write):
    for key in distribution.keys():
        string = str(key) + ","+ str(distribution[key])
        file_write.write(string)
    file_write.close()

# 读文件得取出大于阈值的社团
def read_file(file_path,file):
    file_read = open(file_path,'r',encoding='utf-8')
    read_line = file_read.readlines()
    count = 0
    for line in read_line:
        count += 1
        line_list = line.split(" ")
        number_len = len(line_list)
        if number_len > 20:
            calculate(line,file)
        else:
            continue
    print("finish file " + str(file) +" : ")
    file_read.close()

if __name__ == '__main__':
    star_time = time.time()
    distribution = {}
    file_list = ["06","07","08","09","10","11","12","13","14","15","16","17"]
    for file in file_list:
        file_path = r"F:\classify_data\newMaterials\title_fos\title_fos"+ file +"_both_words_new_result.txt"
        print(file_path)
        read_file(file_path,file)
    print("cost time : " + str(time.time() - star_time))
    file_write = open(r"F:\classify_data\newMaterials\title_fos\cluster_every_year_distribution_data.txt", 'w',
                      encoding='utf-8')
    # distribution = sorted(distribution.keys())
    write_distribution(distribution, file_write)
    # print(distribution)
