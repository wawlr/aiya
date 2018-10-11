## 处理index,name_1,name_2等社团的信息


# -*- coding: utf-8 -*-
# Author: cong
# Copyrigh 2017

# 根据cluster_distribution_data 得到的大于阈值的社团论文的id

# 根据社团的id取得对应的论文，id,doi,year
# 结果写到一个文件里

import time
def main():
    print(time.time())
    name_dic = {}
    name_paper_number_dic = {}
    read_name_file = open("F:\\classify_data\\newMaterials\\index_name.txt",'r',encoding='utf-8')
    read_names = read_name_file.readlines()
    for index_name in read_names:
        index_name = index_name.rstrip("\n")
        index_name_list = index_name.split(",")
        index = index_name_list[0]
        name = index_name_list[1]
        name_dic[name] = index

    for file_i in range(38):
        name_net_dic ={}
        print("del file : " + str(file_i + 1))
        input_path = "F:\\classify_data\\newMaterials\\cluster_data_name\\index_name_"+str(file_i + 1 ) + ".txt"
        input_file = open(input_path,'r',encoding='utf-8')
        readlines = input_file.readlines()
        write_file = open("F:\\classify_data\\newMaterials\\cluster_data_net\\index_name_net_"+str(file_i + 1) + ".txt",'w',encoding='utf-8')
        write_file2 = open("F:\\classify_data\\newMaterials\\cluster_data_net\\name_number_" + str(file_i + 1) + ".txt",
                          'w', encoding='utf-8')
        for line in readlines:
            line = line.rstrip("\n")
            line_list = line.split(",")
            temp_name_list = [] # name_list
            line_list1 = line_list[1:]
            for name in line_list1:
                temp_name_list.append(name)
                # 看作者出现的次数
                if name in name_dic.keys():
                    name_index = name_dic[name]
                    if name_index in name_paper_number_dic.keys():
                        name_paper_number_dic[name_index] += 1
                    else:
                        name_paper_number_dic[name_index] = 1


            for i in range(len(temp_name_list)):
                for j in range(len(temp_name_list)):
                    if j > i:
                        if temp_name_list[i] in name_dic.keys() and temp_name_list[j] in name_dic.keys():
                            # print(temp_name_list[i],temp_name_list[j])
                            index_i = name_dic[temp_name_list[i]]
                            index_j = name_dic[temp_name_list[j]]

                            name_net_i = str(index_i) + "$" + str(index_j)
                            name_net_i_rev = str(index_j) + "$" + str(index_i)
                            # print(name_net_i,name_net_i_rev)
                            if name_net_i in name_net_dic.keys():
                                name_net_dic[name_net_i] += 1
                            elif name_net_i_rev in name_net_dic.keys():
                                name_net_dic[name_net_i_rev] += 1
                            else:
                                name_net_dic[name_net_i] = 1
        for key in name_net_dic.keys():
            number = name_net_dic[key]
            write_str = str(key)
            write_str_list = write_str.split("$")
            write_str2 = " ".join(write_str_list)
            # print(write_str2)
            write_file.write(write_str2 + " " +str(number) + "\n")
        write_file.close()

        # 写出作者出现次数的
        for name_key in name_paper_number_dic.keys():
            str_name = str(name_key) + "," + str(name_paper_number_dic[name_key])+"\n"
            write_file2.write(str_name)
        write_file2.close()

if __name__ == '__main__':
    main()