
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy

from src.databases import mongo_operations
from matplotlib import pyplot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.colors import ListedColormap
from sklearn import datasets
from sklearn.neighbors import NearestCentroid
from sklearn import neighbors

mongo_connection = mongo_operations.get_new_connection_to_database()
collection = mongo_connection.collection


# result=secound_prepare_date()

rc('font', family='Arial')
def secound_prepare_date():
    result = []
    for result_row in collection.find():
        addToResult = False
        for affiliation_dict in result_row['affiliations']:
            if affiliation_dict != 'undefined':
                addToResult = True
                print("true")
        if addToResult:
            result.append(result_row)
            print("appended")
            addToResult = False
    return result


def print_distinct(result):
    lista = []
    for i in result:
        for j in i["affiliations"]:
            lista.append(j)
    dist_list = set(lista)
    dist_list = sorted(dist_list)
    for i in dist_list:
        print(i)


uniRank = {}
keyWordRank = {}
keyWordsDensity = {}


def addUniRangk(uni, keyWord, Year):
    if uni in uniRank:
        if keyWord in uniRank[uni]:
            if Year in uniRank[uni][keyWord]:
                uniRank[uni][keyWord][Year] += 1
            else:
                uniRank[uni][keyWord][Year] = 1
        else:
            uniRank[uni][keyWord] = {}
            addUniRangk(uni, keyWord, Year)
    else:
        uniRank[uni] = {}
        addUniRangk(uni, keyWord, Year)


def addKeywordRank(keyWord, uni, year):
    if keyWord in keyWordRank:
        if uni in keyWordRank[keyWord]:
            if year in keyWordRank[keyWord][uni]:
                keyWordRank[keyWord][uni][year] += 1
            else:
                keyWordRank[keyWord][uni][year] = 1
        else:
            keyWordRank[keyWord][uni] = {}
            addKeywordRank(keyWord, uni, year)
    else:
        keyWordRank[keyWord] = {}
        addKeywordRank(keyWord, uni, year)


def keywordDensity():
    for key in keyWordRank.keys():
        if key in keyWordsDensity:
            pass
        else:
            keyWordsDensity[key] = 0
        for childKey in keyWordRank[key]:
            for secoundChildKey in keyWordRank[key][childKey]:
                keyWordsDensity[key] += keyWordRank[key][childKey][secoundChildKey]


def createTwoColumnTable(h1, h2, list):
    print("{:<40} {:<15}".format(h1, h2))
    for k in list:
        print("{:<40} {:<15} ".format(k[0], k[1]))


def counter(elementSet):
    for publication in elementSet:
        for affiliation in publication["affiliations"]:
            # print(affiliation, publication["year"], publication["key_words"], publication["article_title"])
            for keyWord in publication["key_words"]:
                addUniRangk(affiliation, keyWord, publication["year"])
                addKeywordRank(keyWord, affiliation, publication["year"])


result = secound_prepare_date()
# print(result)     #VIP
counter(result)
# print(len(uniRank.keys()))  #VIP
# for i in uniRank.keys():
#     print(i)
#     print(uniRank[i].keys())
keywordDensity()
keyWordsDensity = sorted(keyWordsDensity.items(), reverse=True, key=lambda value: value[1])
# print(keyWordsDensity)

createTwoColumnTable('Key', 'Label', keyWordsDensity)

# print(len(keyWordRank.keys()))
# for i in keyWordRank.keys():
#     print(i)
#     print(keyWordRank[i].keys())
uniTable = {}
tmpTable = []
keyword1 = "Data Mining"
for i in uniRank.keys():
    if i in uniTable.keys():
        pass
    else:
        uniTable[i] = {}
    if keyword1 in uniRank[i]:
        # print(i)
        # print(sum(uniRank[i][keyword1].values()))
        # print(uniRank[i][keyword1])
        tmpTable.append([i, sum(uniRank[i][keyword1].values()), uniRank[i][keyword1]])
        uniTable[i][keyword1] = sum(uniRank[i][keyword1].values())
keyword2 = "Big Data"

for i in uniRank.keys():
    if i in uniTable.keys():
        pass
    else:
        uniTable[i] = {}
    if keyword2 in uniRank[i]:
        # print(i)
        # print(sum(uniRank[i][keyword2].values()))
        # print(uniRank[i][keyword2])
        tmpTable.append([i, sum(uniRank[i][keyword2].values()), uniRank[i][keyword2]])
        uniTable[i][keyword2] = sum(uniRank[i][keyword2].values())

tmpTable.sort(reverse=True, key=lambda value: value[1])
# for r in tmpTable:
#     print(r)
toPlot = []
labels = []
for i in uniTable:
    if keyword1 in uniTable[i].keys():
        if keyword2 in uniTable[i].keys():
            labels.append(i)
            print(i, uniTable[i])
            toPlot.append([i, uniTable[i][keyword1], uniTable[i][keyword2]])
# print(toPlot)

# cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
# cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
y = []
x = []
for i in toPlot:
    x.append([i[1], i[2]])
    if i[1] >= 5 and i[2] >= 5:
        y.append(0)
    elif i[2] >= 5:
        y.append(1)
    elif i[1] >= 5:
        print("class #")
        y.append(3)
    else:
        y.append(2)
# print("x", x[:])
x = np.array(x[:])
# print(x)
# x = np.ndarray((2,), buffer=x[:])
# print("xnp", x)
print(x.size, len(y))
# print("labels", len(labels))
h = .02
n_neighbors=2
cmap_light = ListedColormap(['#FFAAAA', '#C0F4CC', '#AAAAFF', '#5CB4F2'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF', '#000000'])
for weights in ['uniform']:#, 'distance'
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights, metric='manhattan')
    clf.fit(x, y)
    y_pred = clf.predict(x)
    print(weights, np.mean(y == y_pred))
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
    plt.scatter(x[:, 0], x[:, 1], c=y, cmap=cmap_bold)
    iterator = 0
    cordTab = []
    plt.xlabel(keyword1)
    plt.ylabel(keyword2)

    def addAnnotate(labels, i):
        cord = [i[0], i[1]]
        # print(labels, i, "and cord tab", cordTab,' cord ',cord)
        if cord in cordTab:
            return addAnnotate(labels, numpy.array([i[0], i[1] + .2]))
        elif i[0]==2:
            return addAnnotate(labels, numpy.array([i[0]+.01, i[1] - .4]))
        else:
            plt.annotate(labels, i, textcoords='offset points', ha='left', va='bottom')
            return cord


    for i in x:
        added = addAnnotate(labels[iterator], i)
        cordTab.append(added)  # , textcoords='offset points', ha='left', va='bottom')  # ,
        #  bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        iterator += 1
    plt.title("3-Class classification (k = %i, weights = '%s')"
              % (n_neighbors, weights))
    plt.axis('tight')

plt.show()
