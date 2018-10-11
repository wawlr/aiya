# 处理论文得到论文的信息
# index + 标题
# index + 标题 + 摘要
# index + 摘要 + fos
import time
# !/usr/bin/python
# encoding='utf-8'
import os, time, json

# title_fos
def getfile1(data, fileOut):
    global index
    title = data["title"]
    fileOut.write(str(index) + "," + title)
    if "fos" in data:
        fos = data["fos"]
        fileOut.write(" ")
        fileOut.write(" ".join(fos))
    fileOut.write("\n")

# title_abstract
def getfile2(data, fileOut):
    global index
    title = data["title"]
    fileOut.write(str(index) + "," + title)
    abstract = data["abstract"] if "abstract" in data else""
    fileOut.write(" " + abstract + "\n")
    # venue = data["venue"] if "venue" in data else ""
    # temp_list.append(venue)
    # year = data["year"] if "year" in data else""
    # temp_list.append(str(year))
    # n_citation = data["n_citation"] if "n_citation" in data else""
    # temp_list.append(str(n_citation))
    # doc_type = data["doc_type"] if "doc_type" in data else""
    # temp_list.append(doc_type)
    # lang = data["lang"] if "lang" in data else""
    # temp_list.append(lang)
    # publisher = data["publisher"] if "publisher" in data else""
    # temp_list.append(publisher)
    #
    # fileOut.write(",".join(temp_list))
    # fileOut.write("\n")

# 数据按时间切片：title + fos
# 2012、2013、2014、2015、2016-17
def getfile3(data,fileOut3_06,fileOut3_07,fileOut3_08,fileOut3_09,fileOut3_10,fileOut3_11,fileOut3_12,fileOut3_13,fileOut3_14,fileOut3_15,fileOut3_16,fileOut3_17,fileOut3_nan,fileOut3_other):
    global index
    title = data["title"]
    # fileOut_list = [fileOut3_12,fileOut3_13,fileOut3_14,fileOut3_15,fileOut3_16,fileOut3_nan,fileOut3_other]
    # 拿到年份然后存入
    if "year" in data:
        year = data["year"]
        if str(year) == "2012":
            fileOut = fileOut3_12
        elif str(year) == "2013":
            fileOut = fileOut3_13
        elif str(year) == "2014":
            fileOut = fileOut3_14
        elif str(year) == "2015":
            fileOut = fileOut3_15
        elif str(year) == "2016":
            fileOut = fileOut3_16
        elif str(year) == "2017":
            fileOut = fileOut3_17
        elif str(year) == "2011":
            fileOut = fileOut3_11
        elif str(year) == "2010":
            fileOut = fileOut3_10
        elif str(year) == "2009":
            fileOut = fileOut3_09
        elif str(year) == "2008":
            fileOut = fileOut3_08
        elif str(year) == "2007":
            fileOut = fileOut3_07
        elif str(year) == "2006":
            fileOut = fileOut3_06
        else:
            fileOut = fileOut3_other
    else:
        fileOut = fileOut3_nan
    fileOut.write(str(index) + "," + title)

    if "fos" in data:
        fos = data["fos"]
        fileOut.write(" ")
        fileOut.write(" ".join(fos))
    fileOut.write("\n")


# abstract_fos
def getfile5(data, fileOut):
    global index

    fileOut.write(str(index))
    abstract = data["abstract"] if "abstract" in data else""
    # temp_list.append(abstract)
    fos = data["fos"] if "fos" in data else""
    # temp_list.append(fos)
    fos = " ".join(fos)
    fileOut.write("," + abstract + " "+ fos + "\n")
    # fileOut.write("\n")

# index $ year $ fos
def getfile6(data, fileOut):
    global index
    fileOut.write(str(index))
    # temp_list.append(abstract)
    year = data["year"] if "year" in data else "nan"
    fileOut.write("$" + str(year))
    fos = data["fos"] if "fos" in data else""
    # temp_list.append(fos)
    fos = ",".join(fos)
    fileOut.write("$" + fos + "\n")

    # fileOut.write("\n")

def get_year(data,file_year):
    global index
    global dic_year
    # dic_year = {}
    # file_year.write(str(index))
    year = data["year"] if "year" in data else ""
    if year in dic_year.keys():
        dic_year[year] += 1
    else:
        dic_year[year] = 1
    # for key in dic_year.keys():
    #     str_write = str(key)+","+str(dic_year[key])+"\n"
    #     file_year.write(str_write)
    # file_year.close()
    # return dic_year

# index $ doi $ author $ publisher
def get_author_info(data,fileOut):
    global index
    fileOut.write(str(index))
    # temp_list.append(abstract)
    doi = data["doi"] if "doi" in data else "nan"
    fileOut.write("$" + str(doi))
    authors = data["authors"] if "authors" in data else "nan"
    fileOut.write("$" + str(authors))
    publisher = data["publisher"] if "publisher" in data else "publisher"
    fileOut.write("$" + str(publisher)+"\n")
    # temp_list.append(fos)

# id,doi,year
def get_doi_year(data,fileOut):
    global index
    fileOut.write(str(index))
    # temp_list.append(abstract)
    doi = data["doi"] if "doi" in data else "nan"
    fileOut.write("," + str(doi))
    year = data["year"] if "year" in data else "nan"
    fileOut.write("," + str(year) + "\n")

# index,name_1,name_2
def get_name(data,fileOut):
    global index
    fileOut.write(str(index))
    # temp_list.append(abstract)
    authors = data["authors"] if "authors" in data else "nan"
    name_list = []
    if authors == "nan":
        fileOut.write("," + authors + "\n")
    else:
        for dic in authors:
            name = dic["name"]
            name_list.append(name)
        str_name = ",".join(name_list)
        fileOut.write("," + str_name + "\n")

def get_name_index(data,fileOut):
    global index,name_dic,name_number
    # fileOut.write(str(index))
    # temp_list.append(abstract)
    authors = data["authors"] if "authors" in data else "nan"

    if authors == "nan":
        # fileOut.write("," + authors + "\n")
        print("nan")
    else:
        for dic in authors:
            name = dic["name"]
            if name in name_dic.keys():
                continue
            else:
                name_number += 1
                name_dic[name] = name_number



if __name__ == "__main__":
    time0 = time.time()
    fileNum = 0
    index = 0
    dic_year = {}
    name_dic = {}
    name_number = 0
    directory = "F:\\classify_data\\newMaterials\\oral"
    files = os.listdir(directory)
    fileOut1 = open("F:\\classify_data\\newMaterials\\title_fos.txt", 'w', encoding='utf-8')
    fileOut2 = open("F:\\classify_data\\newMaterials\\title_abstract.txt", 'w', encoding='utf-8')
    fileOut3_06 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos06.txt", 'w', encoding='utf-8')
    fileOut3_07 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos07.txt", 'w', encoding='utf-8')
    fileOut3_08 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos08.txt", 'w', encoding='utf-8')
    fileOut3_09 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos09.txt", 'w', encoding='utf-8')
    fileOut3_10 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos10.txt", 'w', encoding='utf-8')
    fileOut3_11 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos11.txt", 'w', encoding='utf-8')
    fileOut3_12 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos12.txt", 'w', encoding='utf-8')
    fileOut3_13 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos13.txt", 'w', encoding='utf-8')
    fileOut3_14 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos14.txt", 'w', encoding='utf-8')
    fileOut3_15 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos15.txt", 'w', encoding='utf-8')
    fileOut3_16 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos16.txt", 'w', encoding='utf-8')
    fileOut3_17 = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos17.txt", 'w', encoding='utf-8')
    fileOut3_nan = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos_nan.txt", 'w', encoding='utf-8')
    fileOut3_other = open("F:\\classify_data\\newMaterials\\title_fos\\title_fos_other.txt", 'w', encoding='utf-8')

    fileOut5 = open("F:\\classify_data\\newMaterials\\abstract_fos.txt", 'w', encoding='utf-8')
    fileOut6 = open("F:\\classify_data\\newMaterials\\index_year_fos.txt", 'w', encoding='utf-8')
    fileOut_doi_year = open("F:\\classify_data\\newMaterials\\index_doi_year.txt", 'w', encoding='utf-8')
    fileOut_name = open("F:\\classify_data\\newMaterials\\index_name_all.txt", 'w', encoding='utf-8')
    fileOut_name_index = open("F:\\classify_data\\newMaterials\\index_name.txt", 'w', encoding='utf-8')
    fileOut_authors = open("F:\\classify_data\\newMaterials\\author_publisher_info.txt", 'w', encoding='utf-8')

    file_year = open("F:\\classify_data\\newMaterials\\info_year.txt",'w',encoding='utf-8')
    for file in files:
        print(str(file))
        for line in open(directory + "\\" + file, 'r', encoding='utf-8',errors='ignore'):
            # print(line)
            # print(line)
            data = json.loads(line)
            getfile1(data, fileOut1)
            getfile2(data, fileOut2)
            getfile3(data,fileOut3_06,fileOut3_07,fileOut3_08,fileOut3_09,fileOut3_10,fileOut3_11,fileOut3_12,fileOut3_13,fileOut3_14,fileOut3_15,fileOut3_16,fileOut3_17,fileOut3_nan,fileOut3_other)
            getfile5(data, fileOut5)
            getfile6(data, fileOut6)
            get_year(data,file_year)
            get_author_info(data,fileOut_authors)
            get_name(data, fileOut_name)
            get_name_index(data, fileOut_name_index)
            get_doi_year(data, fileOut_doi_year)
            # line = fileIn.readline()
            index += 1
            if index % 10000 == 0:
                print("Have Deal " + str(index) + ". Use Time : " + str(time.time() - time0))
        fileNum += 1
        print("Have Deal " + str(fileNum) + ". Use Time : " + str(time.time() - time0))
    fileOut1.close()
    fileOut2.close()
    fileOut5.close()
    fileOut6.close()
    fileOut_doi_year.close()
    fileOut_name.close()
    for key in name_dic.keys():
        str_write = str(name_dic[key]) + "," + str(key) + "\n"
        # print(key)
        fileOut_name_index.write(str_write)
    fileOut_name_index.close()
    fileOut_authors.close()
    for key in dic_year.keys():
        str_write = str(key)+","+str(dic_year[key])+"\n"
        file_year.write(str_write)
    file_year.close()
    fileOut3_06.close()
    fileOut3_07.close()
    fileOut3_08.close()
    fileOut3_09.close()
    fileOut3_10.close()
    fileOut3_11.close()
    fileOut3_12.close()
    fileOut3_13.close()
    fileOut3_14.close()
    fileOut3_15.close()
    fileOut3_16.close()
    fileOut3_nan.close()
    fileOut3_other.close()