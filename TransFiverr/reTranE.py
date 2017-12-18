#!/usr/bin/env python
# _*_ encoding:utf-8 _*_

from tranE import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def loadData(str):
    fr = open(str)
    sArr = [line.strip().split("\t") for line in fr.readlines()]
    datArr = [[float(s) for s in line[1][1:-1].split(", ")] for line in sArr]
    nameArr = [line[0] for line in sArr]
    dic = {}
    for name, vec in zip(nameArr, datArr):
        dic[name] = array(vec)
    return dic


if __name__ == '__main__':
    dbpath = 'D:/code_py/TransFiverr/data/'
    entityList = loadData(dbpath + 'entityVector.txt')
    relationList = loadData(dbpath + 'relationVector.txt')
    tripleNum, tripleList = openTrain(dbpath + 'train.txt')
    transE = TransE(dbpath, entityList, relationList, tripleList, margin=1, learingRate = 0.001, dim = 100)
    transE.transE(15000)
    transE.writeRelationVector(dbpath + 'relationVector.txt')
    transE.writeEntilyVector(dbpath + 'entityVector.txt')
