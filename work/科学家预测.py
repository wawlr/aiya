#coding=utf-8

from sklearn import linear_model
from pandas import *

#数据导入
scientists = {}
for i in ['02', '03', '04', '05', '06']:
    with open('C:/Users/Administrator/Desktop/datatest/20'+ i +'科学家.txt','r') as f:
        for line in f:
            s = line.strip().split(',')
            if i == '02':
                scientists[s[0]] = [int(s[-2])]
            else:
                scientists[s[0]].append(int(s[-2]))

#线性回归预测
def predictTenYears(scientist):
    clf = linear_model.LinearRegression()
    clf.fit([[1], [2], [3], [4], [5]], scientist[:5])
    return clf.predict(15)
# print predictTenYears(scientists['P. Zoller'])
# print predictTenYears(scientists['J. I. Cirac'])
# print predictTenYears(scientists['Steven Weinberg'])
# print predictTenYears(scientists['P. W. Anderson'])



#预测准确率
scores = {}
for scientist in scientists.keys():
    scores[scientist] = predictTenYears(scientists[scientist])
scores = [x[0] for x in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
s2016 = []
s2006 = {}
with open('C:/Users/Administrator/Desktop/datatest/2016领军人物.txt', 'r') as f:
    for line in f:
        s = line.strip().split(',')
        s2016.append(s[0])

with open('C:/Users/Administrator/Desktop/datatest/2006科学家.txt', 'r') as f:
    for line in f:
        s = line.strip().split(',')
        s2006[s[0]] = int(s[-1])

num = 0
for i in scores[:100]:
    if i in s2016:
        num += 1
print('准确率:', num/100.0)
#
# real = range(1, 101)
# pred = []
# for scientist in s2016:
#     pred.append(scores.index(scientist)+1)
# print pred
# p2006 = []
# for scientist in s2016:
#     p2006.append(s2006[scientist])
# print p2006
# s1 = Series(real) #转为series类型
# s2 = Series(pred)
# s3 = Series(p2006)
# corr1 = s1.corr(s2)
# corr2 = s1.corr(s3)#计算相关系数
# print '相关性', corr1
# print '相关性', corr2