# -*- coding: utf-8 -*-
# Author: cong
# Copyrigh 2017

# 根据cluster_distribution_data 得到的大于阈值的社团论文的id找到对应的论文信息fos+title

# 根据每年的id取得对应的论文，id,fos+title
# 结果写到一个文件里

import time
def main():
    # print(time.time())
    input_path = r"F:\classify_data\newMaterials\title_fos\cluster_every_year_distribution_data.txt"
    input_file = open(input_path,'r',encoding='utf-8')
    ori_input = open(r"F:\classify_data\newMaterials\title_fos.txt",'r',encoding='utf-8')
    ori_lines = ori_input.readlines()
    readlines = input_file.readlines()

    output_file = open(r"F:\classify_data\newMaterials\title_fos\fos_title_every_year_data.txt",'w',encoding='utf-8')

    for line in readlines:
        line_list = line.split(",")
        year = line_list[0] # 年份
        lines = line_list[1].strip("\n")
        lines_list = lines.split(" ")
        for id in lines_list:
            if id == "":
                continue
            # print(id)
            id = int(id)
            # print(ori_lines[id])
            output_file.write(ori_lines[id])
    output_file.close()
    ori_input.close()
    input_file.close()
    print("finish.")
if __name__ == '__main__':
    main()