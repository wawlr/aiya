# 找到最多论文的社团
import time
if __name__ == '__main__':
    start_time = time.time()
    print("start happy :" +str(start_time))
    file_name = "newMaterials"
    file_list = [16,20,21,22,25,30,36]
    for file_i in file_list:
        name_number_dic = {}
        read_file = open("F:\\classify_data\\"+ file_name +"\\cluster_data_net\\name_number_" + str(file_i) + ".txt",
                              'r', encoding='utf-8')
        read_file_lines = read_file.readlines()
        for line in read_file_lines:
            line_list = line.split(",")
            name = line_list[0]
            number = line_list[1].rstrip("\n")
            name_number_dic[name] = number

        read_file_cluster = open("F:\\classify_data\\"+ file_name +"\\cluster_data_net\\index_name_net_" + str(file_i) + "_new_result.txt",
                              'r', encoding='utf-8')
        read_file_cluster_lines = read_file_cluster.readlines()

        write_file_cluster = open("F:\\classify_data\\"+ file_name +"\\cluster_data_net\\index_name_net_" + str(file_i) + "_new_result_write.csv",
                                'w', encoding='utf-8')

        for line2 in read_file_cluster_lines:
            number_line2 = 0
            line2 = line2.rstrip("\n")
            line_list2 = line2.split(" ")
            for name2 in line_list2:
                # print(name2)
                # print(name_number_dic.keys())
                if name2 in name_number_dic.keys():
                    number_line2  = number_line2 + int(name_number_dic[name2])
                    # print("ok")
            str_write = str(number_line2) + "," +line2 + "\n"
            write_file_cluster.write(str_write)
        write_file_cluster.close()
