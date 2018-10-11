# -*- coding: utf-8 -*-
# Author: cong
# Copyrigh 2018

# 根据小领域的fos核心词，找到领域论文数目的按年度的变化趋势。

import time
import math
import matplotlib.pyplot as plt
import numpy as np

def calculate(line, words_list):
    global fos_year_dist_dic,year_str,number_str
    line_list = line.split("$")
    # print(line_list)
    index = line_list[0]
    year = line_list[1]
    fos_words = line_list[2].rstrip("\n")
    fos_words_list = fos_words.split(",")
    temp_list = []
    for word in fos_words_list:
        temp_list.append(word.lower())
    # print(words_list)
    # print(temp_list)
    # print(set(fos_words_list) & set(words_list))
    if len(set(temp_list) & set(words_list)) > 2:
        # 存入年份趋势字典
        # print(set(temp_list) & set(words_list))
        if year in fos_year_dist_dic.keys():
            fos_year_dist_dic[year] = fos_year_dist_dic[year] + 1
        else:
            fos_year_dist_dic[year] = 1

def main():
    global fos_year_dist_dic,year_str,number_str,ratio_str,log_2_ratio_str,log_e_ratio_str,log_10_ratio_str
    print("start: " + str(time.time()))
    start_time = time.time()
    ##  读入fos总的社团划分的文件，处理得到词链表，用来做趋势

    # 读入年份和总的论文数目
    year_number_file = open(r"F:\classify_data\newMaterials\info_year.txt", 'r', encoding='utf-8')
    year_number_lines = year_number_file.readlines()
    year_number_dic = {}
    # 年份和总的论文数目信息存入字典中
    for year_number_line in year_number_lines:
        year_number_list = year_number_line.split(",")
        year_number_dic[year_number_list[0]] = year_number_list[1].rsplit("\n")
    # 画图年份信息，横坐标
    year_number_trule = [v for v in sorted(year_number_dic.items(), key=lambda d: d[0])]
    year_number_trule_list = []
    for item in year_number_trule:
        year_number_trule_list.append(item[0])

    # 读入索引、fos和年份
    index_year_fos_file = open(r"F:\classify_data\newMaterials\index_year_fos.txt", 'r', encoding='utf-8')
    # 结果文档
    index_year_fos = index_year_fos_file.readlines()
    file_write = open(r"F:\classify_data\newMaterials\year_distribution.csv", 'a', encoding='utf-8')
    # 读入fos词语社团划分结果
    index_fos_result_fos_file = open(r"F:\classify_data\newMaterials\title_fos\06_17_index_fos_result_fos.txt","r",encoding='utf-8')
    index_fos_result_fos = index_fos_result_fos_file.readlines()

    # 画图
    # 第一个参数表示的是编号，第二个表示的是图表的长宽
    plt.figure(num=1, figsize=(8, 5))
    plot_year_dic = {}
    plot_index_dic = {}
    max_value = []

    line_index = 0
    for fos_line in index_fos_result_fos:
        line_index += 1
        if fos_line != "":
            fos_line_list = fos_line.split(",")
            fos_line_list[-1] = fos_line_list[-1].strip("\n")
            temp_list = ["Cluster_"+str(line_index)]
            cluster_name = "Cluster_"+str(line_index)# 画图的名称
            temp_list.extend(fos_line_list[4:])
            # print(temp_list)

            # fos_words_list = ["machine learning","data mining","artificial intelligence","artificial neural network","theoretical computer science","data science","time delay neural network","probabilistic neural network","pattern recognition","mathematical optimization","recurrent neural network","data analysis","stochastic neural network","organizational network analysis","data modeling"]
            # fos_words_list = ["cell biology","anatomy","cellular differentiation","immunology","stem cell","embryonic stem cell","bioinformatics","cell culture","cell growth","biochemistry","induced pluripotent stem cell","gene expression","pathology","mesenchymal stem cell"]
            # fos_words_list = ["virology","dna repair","dna damage","dna replication","cell biology","cell culture","dna","viral replication","bioinformatics","dna-binding protein","genome instability","replication protein a","cell cycle","mutation","eukaryotic dna replication","proliferating cell nuclear antigen","origin recognition complex","enzyme","dna polymerase"]
            # fos_words_list = ["signal transduction","phosphorylation","immunology","cancer research","mitogen-activated protein kinase","bioinformatics","endocrinology","protein kinase a","protein kinase c","cell culture","protein kinase b","p70s6 kinase","enzyme activator","enzyme","cyclin-dependent kinase 2","mitogen-activated protein kinase kinase","cell growth"," map2k7","extracellular signal-regulated kinases","apoptosis"]
            # fos_words_list = ["dna microarray","proteomics","genomics","gene expression profiling","gene expression","genome","botany","whole genome sequencing","biotechnology","transcriptome","dna sequencing","comparative genomics","gene","sequence alignment","genetic variation","regulation of gene expression","human genetics","dna","mutation","genotype","microbiology","cluster analysis","microarray analysis techniques","microrna","comparative genomic hybridization","phenotype","signal transduction","pathology","genome evolution","expressed sequence tag","phylogenetics","gene duplication","genomic library","high-throughput screening","the internet","immunology","copy-number variation","sequence analysis","genome project","human genome","ecology","polymorphism","transcription factor"]
            fos_words_list = temp_list
            for line in index_year_fos:
                # line_list = line.split("$")
                calculate(line, fos_words_list)
            # print(fos_year_dist_dic)

            fos_year_dist_list = [v for v in sorted(fos_year_dist_dic.items(), key=lambda d: d[0])]
            # 画图数据
            plot_year = []
            plot_index = []
            for item in fos_year_dist_list:
                plot_year.append(item[0])
                year = item[0]
                number = item[1]
                all_number = year_number_dic[year]
                year_str = year_str + "," + str(year)
                number_str = number_str + "," + str(number)
                ratio_str = ratio_str + "," + str(number/int(all_number[0]))
                # log 2,e,10 的数值
                log_2_ratio = number/int(all_number[0]) * math.log(max((number - 2),1),2)
                log_e_ratio = number/int(all_number[0]) * math.log(max((number - 2),1),math.e)
                log_10_ratio = number/int(all_number[0]) * math.log(max((number - 2),1),10)
                log_2_ratio_str = log_2_ratio_str + "," + str(log_2_ratio)
                log_e_ratio_str = log_e_ratio_str + "," + str(log_e_ratio)
                log_10_ratio_str = log_10_ratio_str + "," + str(log_10_ratio)
                plot_index.append(log_10_ratio)# 画图指数的纵坐标
            if len(plot_index)> 0:
                max_value.append(max(plot_index))
            # 画图数据
            plot_year_dic[cluster_name] = plot_year
            plot_index_dic[cluster_name] = plot_index

            # print(year_str[1:])
            # print(number_str[1:])
            # print(ratio_str[1:])
            file_write.write(",".join(fos_words_list) + "\n")
            write_string = year_str[1:] + "\n" + number_str[1:] + "\n" + ratio_str[1:] + "\n" + log_2_ratio_str[1:] + "\n"+log_e_ratio_str[1:]+"\n"+log_10_ratio_str[1:]+"\n"+"\n"
            # write_string = year_str[1:] + "\n" + ratio_str[1:] + "\n"
            file_write.write(write_string)
            # 清空初始化
            year_str = ""
            number_str = ""
            ratio_str = ""
            log_2_ratio_str = ""
            log_e_ratio_str = ""
            log_10_ratio_str = ""
            fos_year_dist_dic = {}

            print("finish  "+str(cluster_name)+"  " + str( time.time() - start_time))
            # file_write.close()
            # index_year_fos_file.close()
    # 画图
    # 设置取值参数
    plt.xlim(1960, int(year_number_trule_list[-1]))
    plt.ylim((0,max(max_value)*1.2))
    # 设置lable
    plt.xlabel("year")
    plt.ylabel("hot index")
    # 设置点的位置
    new_ticks = np.linspace(1960, int(year_number_trule_list[-1]),
                            int((int(year_number_trule_list[-1]) - 1960) / 5))
    new_ticks2 = np.linspace(0, int(max(max_value)*120)/100,5)
    plt.xticks(new_ticks)
    plt.yticks(new_ticks2)

    plot_l_list = []
    color_list = ['r','b','c','k','y','r','b','c','k','y']
    linestyle_list = ['-.','--',':','-','-.','--',':','-']
    list_i = 0
    for cluster_name in plot_year_dic.keys():
        lx, = plt.plot(plot_year_dic[cluster_name], plot_index_dic[cluster_name],
                       color=color_list[list_i],  # 线条颜色
                       linewidth=1.0,  # 线条宽度
                       linestyle=linestyle_list[list_i],  # 线条样式
                       label= cluster_name  # 标签
                       )
        list_i += 1
        plot_l_list.append(lx)
    # 使用ｌｅｇｅｎｄ绘制多条曲线
    plt.legend(handles=plot_l_list,
               labels=list(plot_year_dic.keys()),
               loc='best'
               )

    plt.show()

if __name__ == '__main__':
    fos_year_dist_dic = {}
    year_str = ""
    number_str = ""
    ratio_str =""
    log_2_ratio_str = ""
    log_e_ratio_str = ""
    log_10_ratio_str = ""
    main()