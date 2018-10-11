# Author: cong
# Copyrigh 2017

# 根据getBigCluster得到人名ID找到对于的名字全称
# 结果写到一个文件里

import time
def main():
    print(time.time())
    file_name = "newMaterials"
    name_dic = {}
    name_paper_number_dic = {}
    # 读入姓名字典
    # key 是数字id，名字是value
    read_name_file = open("F:\\classify_data\\"+ file_name + "\\index_name.txt",'r',encoding='utf-8')
    read_names = read_name_file.readlines()
    for index_name in read_names:
        index_name = index_name.rstrip("\n")
        index_name_list = index_name.split(",")
        index = index_name_list[0]
        name = index_name_list[1]
        name_dic[index] = name

    file_list = [16,20,21,22,25,30,36]
    for file_i in file_list:
        read_file = open("F:\\classify_data\\"+ file_name +"\\cluster_data_net\\index_name_net_" + str(file_i) + "_new_result_write.csv",
                         'r', encoding='utf-8')
        write_file = open(
            "F:\\classify_data\\" + file_name + "\\cluster_data_net\\index_name_net_" + str(file_i) + "_new_result_write_name.csv",
            'w', encoding='utf-8')

        read_file_lines = read_file.readlines()
        for line in read_file_lines:
            # print(line)
            line2 = line.rstrip("\n")
            line_list = line2.split(",")
            cluster_id = line_list[0]
            cluster_name_id = line_list[1]
            cluster_name_id_list = cluster_name_id.split(" ")
            name_list = []
            # print(cluster_name_id_list)
            for name_id in cluster_name_id_list:
                if name_id != "":
                    name_list.append(name_dic[name_id])
            write_str = str(cluster_id)+"," + ",".join(name_list) + "\n"
            write_file.write(write_str)
        write_file.close()

if __name__ == '__main__':
    main()