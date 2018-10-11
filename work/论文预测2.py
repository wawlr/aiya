#coding=utf-8

import datetime
import json

import xlrd
from matplotlib import pyplot as plt
from networkx import *

import numpy as np


def transCite(s):
    s = s.replace('\u003c作　　者 ', "")
    s = s.replace('\u003e', "")
    s = s.replace(',标　　题', "*")
    s = s.replace(',发表日期 ', "*")
    s = s.replace(',期　　刊 ', "*")
    s = s.replace(',被 引 量 ', "*")
    s = s.replace(',DOI', "*")
    return s.split('*')

def transCiteN(s):
    s = s.replace('\u003c ', "")
    s = s.replace('\u003e', "")
    return s.split(';')

def transTwitter(twitters):
    Twitter = {}
    for t in twitters:
        try:
            time = int(t['time'][-5:-1])
            if time in Twitter.keys():
                Twitter[time] += int(t['followernum'].replace(',', ''))/10000.0
            else:
                Twitter[time] = int(t['followernum'].replace(',', ''))/10000.0
        except ValueError:
            pass
    return Twitter

def transMedia(medias):
    Media = {}
    for t in medias:
        try:
            time = int(t['time'][-4:])
            if time in Media.keys():
                Media[time] += 1
            else:
                Media[time] = 1
        except ValueError:
            pass
    return Media

def transUsage(usages,l):
    use = {}
    s = [0.2, 0.4, 0.4]
    for i in range(0, len(usages), l):
        time = int(usages[i][-4:])
        if time in use.keys():
            for j in range(1, l):
                use[time] += s[j-1]*int(usages[i+j])
        else:
            use[time] = 0
            for j in range(1, l):
                use[time] += s[j-1]*int(usages[i+j])
    return use

def findImpact(publisher, impactScore):
    s = publisher.upper()
    if s in impactScore.keys():
        return (s, impactScore[s])
    else:
        return (s, 0)

def dataConduction(fileName, type):
    null = ''
    workbook = xlrd.open_workbook('2015SCI.xlsx')
    booksheet = workbook.sheet_by_name('Original IF by IF ')
    impactScore = {}
    for row in range(1, booksheet.nrows):
        if booksheet.cell(row, 3).value != '':
            impactScore[str(booksheet.cell(row, 0).value)] = int(booksheet.cell(row, 3).value)
        else:
            impactScore[str(booksheet.cell(row, 0).value)] = 0
    outputFile = open('paperData', 'a')
    if type == 'N':
        with open(fileName, 'r') as f:
            for line in f:
                content = eval(line)
                if 'Cite' in content.keys() and '(' in content['PaperInfo']:
                    tempNatureDict = {}
                    tempNatureDict['doi'] = content['doi'].split(':')[-1]
                    tempNatureDict['author'] = content['Author']
                    tempNatureDict['publisher'] = findImpact('NATURE', impactScore)
                    tempNatureDict['date'] = int(content['PaperInfo'][-5:-1])
                    if tempNatureDict['date']<2006:
                        continue
                    tempNatureDict['cite'] = []
                    tempNatureDict['twitter'] = ''
                    if 'twitter'in content.keys():
                        tempNatureDict['twitter'] = transTwitter(content['twitter']['twitter'])
                    tempNatureDict['facebook'] = ''
                    if 'facebook'in content.keys():
                        tempNatureDict['facebook'] = transMedia(content['facebook']['facebook'])
                    tempNatureDict['wikipedia'] = ''
                    if 'wikipedia' in content.keys():
                        tempNatureDict['wikipedia'] = transMedia(content['wikipedia']['wikipedia'])
                    tempNatureDict['blogs'] = ''
                    if 'blogs' in content.keys():
                        tempNatureDict['blogs'] = transMedia(content['blogs']['blogs'])
                    tempNatureDict['news'] = ''
                    if 'news' in content.keys():
                        tempNatureDict['news'] = transMedia(content['news']['news'])
                    tempNatureDict['google'] = ''
                    if 'google' in content.keys():
                        tempNatureDict['google'] = transMedia(content['google']['googleplus'])
                    tempNatureDict['Article_usage'] = ''
                    for cite in content['Cite']:
                        if cite['doi'] != '':
                            cite.pop('title')
                            cite.pop('authors')
                            cite['time'] = int(cite['time'])
                            if cite['time'] < 1000:
                                continue
                            cite['citeNum'] = int(cite['citeNum'])
                            cite['publisher'] = findImpact(cite['publisher'], impactScore)
                            tempNatureDict['cite'].append(cite)
                    outputFile.write(json.dumps(tempNatureDict))
                    outputFile.write('\n')
    else:
        with open(fileName, 'r') as f:
            for line in f:
                content = eval(line)
                tempNatureDict = {}
                tempNatureDict['doi'] = content['DOI']
                tempNatureDict['author'] = content['Authors']
                tempNatureDict['publisher'] = findImpact('science', impactScore)
                tempNatureDict['date'] = int(content['Date']['year'])
                if tempNatureDict['date'] < 2006:
                    continue
                tempNatureDict['cite'] = []
                tempNatureDict['twitter'] = ''
                if content['Tweeter'] != '':
                    tempNatureDict['twitter'] = transTwitter(content['Tweeter']['twitter'])
                tempNatureDict['facebook'] = ''
                if content['facebook'] != '':
                    tempNatureDict['facebook'] = transMedia(content['facebook']['facebook'])
                tempNatureDict['wikipedia'] = ''
                if content['wikipedia'] != '':
                    tempNatureDict['wikipedia'] = transMedia(content['wikipedia']['wikipedia'])
                tempNatureDict['blogs'] = ''
                if content['Blogs'] != '':
                    tempNatureDict['Blogs'] = transMedia(content['Blogs']['blogs'])
                tempNatureDict['news'] = ''
                if content['news'] != '':
                    tempNatureDict['news'] = transMedia(content['news']['news'])
                tempNatureDict['google'] = ''
                if content['googleplus'] != '':
                    tempNatureDict['google'] = transMedia(content['googleplus']['googleplus'])
                tempNatureDict['Article_usage'] = ''
                if content['Article_usage'] != '':
                    tempNatureDict['Article_usage'] = transUsage(content['Article_usage'], len(content['Tablehead']))
                for cite in content['Cited'].split('\u003e\u003c作　　者 '):
                    if cite != '':
                        try:
                            c = transCite(cite)
                            if len(c) < 5:
                                continue
                            citeTempDict = {}
                            citeTempDict['doi'] = c[-1]
                            citeTempDict['publisher'] = findImpact(c[-3].replace(' \u0026 ', ' '), impactScore)
                            citeTempDict['time'] = int(c[-4])
                            if citeTempDict['time'] < 1000:
                                continue
                            citeTempDict['citeNum'] = int(c[-2])
                            tempNatureDict['cite'].append(citeTempDict)
                        except ValueError:
                            pass
                outputFile.write(json.dumps(tempNatureDict))
                outputFile.write('\n')
    outputFile.close()
# dataConduction('nature_1.json', 'N')
# dataConduction('nature_2.json', 'N')
# dataConduction('scienceOld', 'S')
# dataConduction('scienceNew', 'S')
# dataConduction('sciencedata0120.json', 'S')
# dataConduction('sicence0202.json', 'S')
def constractG(fileName):
    paperCitationG = nx.DiGraph()  # 指向papers, 入度代表论文被引用数量
    paperAuthorG = nx.DiGraph()  # 指向papers，author节点出度代表发表论文
    with open(fileName, 'r') as f:
        for line in f:
            content = eval(line)
            medias = {}
            medias['twitter'] = content['twitter']
            medias['facebook'] = content['facebook']
            medias['wikipedia'] = content['wikipedia']
            medias['blogs'] = content['blogs']
            medias['news'] = content['news']
            medias['google'] = content['google']
            paperCitationG.add_node(content['doi'], group=1, date=content['date'], publisher=content['publisher'],
                                    medias=medias, usage=content['Article_usage'])

            for cite in content['cite']:#['publisher', 'doi', 'citeNum', 'title', 'time', 'authors']
                if paperCitationG.has_node(cite['doi']):
                    paperCitationG.add_edge(cite['doi'], content['doi'], time=cite['time'] - content['date'], weight=0.9** (
                        cite['time'] - content['date']))
                else:
                    paperCitationG.add_node(cite['doi'], group=0, date=cite['time'], publisher=cite['publisher'], citeNum=cite['citeNum'])
                    paperCitationG.add_edge(cite['doi'], content['doi'], time=cite['time'] - content['date'], weight=0.9** (
                    cite['time'] - content['date']))
    return paperCitationG



def transDate(d):
    return d['year']+'-'+d['month']+'-'+d['day']

def citationTime(d1, d2):#引用时间，以天为单位
    d1 = datetime.datetime.strptime(d1, '%Y-%b-%d')
    d2 = datetime.datetime.strptime(d2, '%Y-%b-%d')
    delta = d1 - d2
    return delta.days


def networkBefore(G, time):#time时刻的网络
    nodes = []
    for paper in G.nodes():
        if G.node[paper]['date'] <= time:
            nodes.append(paper)
    return G.subgraph(nodes)

def citesOfPaper(pCG, K):  # K天内的引用
    papersKCitations = {}
    for paper in pCG.nodes():
        if pCG.node[paper]['group'] == 1:
            cites = 0
            for cite in pCG.in_edges(paper, data=True):
                if cite[2]['time'] < K:
                    cites += 1
            papersKCitations[paper] = cites
    return papersKCitations


def normalization(d):
    Max = max(d.values())
    Min = min(d.values())
    if Max == 0:
        return dict((k, 0) for k, v in d.items())
    return dict((k, (v - Min)/float(Max-Min)) for k, v in d.items())

def paperScore(paperCitationG):
    group = filter(lambda x: x[1]['group'] == 1, paperCitationG.nodes(data=True))
    publisher = dict((k, v['publisher'][1]) for k, v in paperCitationG.nodes(data=True))
    p = nx.pagerank(paperCitationG)
    # pagerank指数
    pagerankScore = normalization(dict((k, v * paperCitationG.number_of_nodes()) for k, v in p.items()))

    #高质量引用
    highQulityCites = dict((k[0], 0) for k in group)
    for paper in group:
        for cite in paperCitationG.in_edges(paper[0], data=True):
            if publisher[cite[0]] > 10:
                highQulityCites[paper[0]] += 1
    highQulityCites = normalization(highQulityCites)

    #altmetric指数
    altmetricScore = dict((k[0], 0) for k in group)
    for paper in group:
        if paper[1]['medias']['twitter'] != '':
            altmetricScore[paper[0]] += sum(paper[1]['medias']['twitter'].values())
        if paper[1]['medias']['facebook'] != '':
            altmetricScore[paper[0]] += int(0.25*sum(paper[1]['medias']['facebook'].values()))
        if paper[1]['medias']['wikipedia'] != '':
            altmetricScore[paper[0]] += 3*sum(paper[1]['medias']['wikipedia'].values())
        if paper[1]['medias']['blogs'] != '':
            altmetricScore[paper[0]] += 5*sum(paper[1]['medias']['blogs'].values())
        if paper[1]['medias']['news'] != '':
            altmetricScore[paper[0]] += 8*sum(paper[1]['medias']['news'].values())
        if paper[1]['medias']['google'] != '':
            altmetricScore[paper[0]] += sum(paper[1]['medias']['google'].values())
    altmetricScore = normalization(altmetricScore)

    #usage指数
    usageScore = dict((k[0], 0) for k in group)
    for paper in group:
        if paper[1]['usage'] != '':
            usageScore[paper[0]] = sum(paper[1]['usage'].values())
    usageScore = normalization(usageScore)

    Score = dict((k[0], 0) for k in group)
    for paper in group:
        Score[paper[0]] = 0.4*pagerankScore[paper[0]] + 0.3*altmetricScore[paper[0]] + 0.2*highQulityCites[paper[0]] + 0.1*usageScore[paper[0]]
    return Score

def makeData(paperCitationG, top):
    Date = nx.get_node_attributes(paperCitationG, 'date')
    group = filter(lambda x: x[1]['group'] == 1, paperCitationG.nodes(data=True))
    publisher = dict((k, v['publisher'][1]) for k, v in paperCitationG.nodes(data=True))
    data = []
    allTimePageRank = {}
    for paper in group:
        temp = [paper[0]]
        date = Date[paper[0]]
        temp.append(date)
        if date + 2 not in allTimePageRank.keys():
            np = networkBefore(paperCitationG, date + 2)
            tempPageRank = dict(
                (k, v * np.number_of_nodes()) for k, v in nx.pagerank(np).items())
            temp.append(tempPageRank[paper[0]])
            allTimePageRank[date + 2] = tempPageRank
        else:
            temp.append(allTimePageRank[date + 2][paper[0]])

        # 高质量引用
        highQulityCites = 0
        for cite in paperCitationG.in_edges(paper[0], data=True):
            if publisher[cite[0]] > 10:
                highQulityCites += 1
        temp.append(highQulityCites)


        altmetric = 0
        if paper[1]['medias']['twitter'] != '':
            altmetric += sum([x[1] for x in filter(lambda x: int(x[0]) <= date + 2, paper[1]['medias']['twitter'].items())])
        if paper[1]['medias']['facebook'] != '':
            altmetric += int(0.25*sum([x[1] for x in filter(lambda x: int(x[0]) <= date + 2, paper[1]['medias']['facebook'].items())]))
        if paper[1]['medias']['wikipedia'] != '':
            altmetric += 3*sum([x[1] for x in filter(lambda x: int(x[0]) <= date + 2, paper[1]['medias']['wikipedia'].items())])
        if paper[1]['medias']['blogs'] != '':
            altmetric += 5*sum([x[1] for x in filter(lambda x: int(x[0]) <= date + 2, paper[1]['medias']['blogs'].items())])
        if paper[1]['medias']['news'] != '':
            altmetric += 8*sum([x[1] for x in filter(lambda x: int(x[0]) <= date + 2, paper[1]['medias']['news'].items())])
        if paper[1]['medias']['google'] != '':
            altmetric += sum([x[1] for x in filter(lambda x: int(x[0]) <= date + 2, paper[1]['medias']['google'].items())])
        temp.append(altmetric)

        if paper[1]['usage'] != '':
            temp.append(sum([x[1] for x in filter(lambda x: int(x[0]) <= date + 2, paper[1]['usage'].items())]))
        else:
            temp.append(0)
        if paper[0] in top:
            temp.append(1)
        else:
            temp.append(0)
        data.append(temp)
    return data


def makeData2(paperCitationG, top):
    Date = nx.get_node_attributes(paperCitationG, 'date')
    group = filter(lambda x: x[1]['group'] == 1, paperCitationG.nodes(data=True))
    publisher = dict((k, v['publisher'][1]) for k, v in paperCitationG.nodes(data=True))
    data = []
    allTimePageRank = {}
    for paper in group:
        temp = [paper[0]]
        date = Date[paper[0]]
        temp.append(date)
        if date + 2 not in allTimePageRank.keys():
            np = networkBefore(paperCitationG, date + 2)
            tempCites = dict(
                (k, v * np.number_of_nodes()) for k, v in nx.in_degree_centrality(np).items())
            temp.append(tempCites[paper[0]])
            allTimePageRank[date + 2] = tempCites
        else:
            temp.append(allTimePageRank[date + 2][paper[0]])

        if paper[0] in top:
            temp.append(1)
        else:
            temp.append(0)

        data.append(temp)
    return data


def  citeWithTime(paper, paperCitationG):
    cites = [0]*11
    for cite in paperCitationG.in_edges(paper, data=True):
        if -1< cite[2]['time'] < 10:
            cites[cite[2]['time']+1] += 1
    for i in range(len(cites)-1):
        cites[i+1] = cites[i] + cites[i+1]
    plt.plot(range(len(cites)), cites)
    plt.show()
if __name__ == "__main__":
    paperCitationG = constractG('C:/Users/Administrator/Desktop/datatest/paperdata')
    # group = filter(lambda x: x[1]['group'] == 1, paperCitationG.nodes(data=True))
    # Score = paperScore(paperCitationG)
    # top = [x[0] for x in sorted(Score.items(), key=lambda x:x[1], reverse=True)[:450]]

    top = []
    file = open('C:/Users/Administrator/Desktop/datatest/正样本', 'r')
    for i in file.readlines():
        top.append(i.strip())
    file.close()


    data = makeData2(paperCitationG, top)
    X = np.array([x[:-1] for x in data])
    np.save("X.npy", X)
    Y = np.array([x[-1] for x in data])
    np.save("Y.npy", Y)

    X = np.load("X.npy")
    Y = np.load("Y.npy")
    Y.reshape(-1, 1)
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=.4, random_state=0)
    y_train.reshape(-1, 1)
    y_test.reshape(-1, 1)
    from sklearn.preprocessing import StandardScaler

    sc = StandardScaler()
    sc.fit(X_train[:, 1:])
    X_train_std = sc.transform(X_train[:, 1:])
    X_test_std = sc.transform(X_test[:, 1:])
    #
    from sklearn.linear_model import LogisticRegression
    from sklearn import metrics
    # from sklearn import svm

    lr = LogisticRegression(C=1000.0, random_state=0)
    # clf = svm.SVC()
    sampleWeight = []
    for i in range(len(X_train_std)):
        if y_train[i] == 1:
            sampleWeight.append(0.6)
        else:
            sampleWeight.append(0.4)
    sampleWeight = np.array(sampleWeight)
    sampleWeight.reshape(-1, 1)
    lr.fit(X_train_std, y_train, sample_weight=sampleWeight)
    # clf.fit(X_train_std, y_train, sample_weight=sampleWeight)
    # for i in range(len(X_test)):
    #     if y_test[i] == 1:
    #         print X_test[i, 0], clf.predict(X_test_std[i]), X_test[i, 1:]
    # y_pred = clf.predict(X_test_std)

    y_pred = lr.predict(X_test_std)

    print(metrics.classification_report(y_test, y_pred))


    #
    #
    #
    #

    # twitterScore = dict((k, sum(v['twitter'].values())) for k, v in group if v['twitter'] != '')
#     paperCitationG = constractScienceG()
#     Date = nx.get_node_attributes(paperCitationG, 'date')
#     group = nx.get_node_attributes(paperCitationG, 'group')
#     p = Pagerank(paperCitationG, alpha=0.5)
#     pagerankScore = dict((k, v * paperCitationG.number_of_nodes()) for k, v in p.items())
#     g1 = {}
#     for node in group:
#         if group[node] == 1:
#             g1[node] = pagerankScore[node]
#     g1 = sorted(g1.items(), key=lambda x: x[1], reverse=True)
#     top = [x[0] for x in g1[:10]]
#     for i in top:
#         np1 = networkBefore(paperCitationG, Date[i]+1)
#         np2 = networkBefore(paperCitationG, Date[i] + 2)
#         print i, Pagerank(np1, alpha=0.5, tol=1.0e-5)[i]*np1.number_of_nodes(), Pagerank(np2, alpha=0.5, tol=1.0e-5)[i] * np2.number_of_nodes()
