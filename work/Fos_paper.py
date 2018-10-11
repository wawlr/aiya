# -*- coding: utf-8 -*-
"""
@Time:2018/7/31 15:09
@Author:wangcong
一想到有那么多痴心姑娘等我，我的良心便有些痛。
"""
import time
import os, time, json

if __name__ == '__main__':

    time0 = time.time()
    fileNum = 0
    index = 0
    number = 0
    dic_year = {}
    name_dic = {}
    name_number = 0
    directory = "F:\\paper\\mag_papers_8"
    files = os.listdir(directory)
    file_write = open("C:\\Users\\Administrator\\Desktop\\computer_science\\small_computer_science8.json",'w',encoding='utf-8')
    fos_list1 = ["artificial intelligence"]
    fos_list2 = ["computer science","artificial intelligence"]
    for file in files:
        print(str(file))
        for line in open(directory + "\\" + file, 'r', encoding='utf-8',errors='ignore'):
            # print(line)
            # line = fileIn.readline()
            index += 1
            data = json.loads(line)
            fos = data["fos"] if "fos" in data else""
            # print(fos)
            if fos != "":

                for f in fos:
                    if f.lower() in fos_list2:
                        # print(f)
                        data_json = json.dumps(data)
                        # print(data_json)
                        file_write.write(data_json)
                        file_write.write("\n")
                        number += 1
                    else:
                        continue
            else:
                continue
            if index % 10000 == 0:
                print("Have Deal " + str(index) + ". Use Time : " + str(time.time() - time0))
            if index % 100000 == 0:
                print("have find :" + str(number))
                print("Have Deal " + str(index) + ". Use Time : " + str(time.time() - time0))

        fileNum += 1
        print("Have Deal " + str(fileNum) + ". Use Time : " + str(time.time() - time0))

    print("have find :" + str(number))
    file_write.close()


def getFosPaper(line,fos_lists):
    fos = line["fos"] if "fos" in data else""
    print(fos)
    if fos != "":
        fos_l = fos.split(",")
        print(fos_l)
        for f in fos_l:
            if f in fos_lists:
                return True
            else:
                continue
        else:
            return False