#!/usr/bin/env python
# _*_ encoding:utf-8 _*_

from numpy import *
import MySQLdb
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


def queryByTag(tagList, entityDic, relationDic):
    relaVec = relationDic['_has_tag']
    res = {}
    for entity in entityDic:
        if entity.startswith('/gig'):  # 只遍历gig
            loss = 0
            for tag in tagList:
                tag = '/tag/' + tag
                loss += linalg.norm(entityDic[entity] + relaVec - entityDic[tag])
            res.setdefault(entity, loss)
    sortList = sorted(res.items(), lambda x, y: cmp(x[1], y[1]))
    return sortList[0:100]


def getDetail(sortList):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "1234", "fiverr")
    res = []
    cursor = db.cursor()
    sql = "SELECT id,title,description,tags,sub_category,category FROM gig_property WHERE id=%s"
    for gig in sortList:
        gid = gig[0][5:]
        cursor.execute(sql, gid)
        row = cursor.fetchone()
        tmp = [str(s) for s in row]
        tmp.append(str(gig[1]))
        res.append(tmp)
    return res


if __name__ == '__main__':
    dbpath = 'D:/code_py/TransFiverr_L2/data/bak/'
    entityDic = loadData(dbpath + 'entityVector.txt')
    relationDic = loadData(dbpath + 'relationVector.txt')
    tags = ['php', 'cms', 'website', 'responsive', 'build website']
    sortList = queryByTag(tags, entityDic, relationDic)
    res = getDetail(sortList)
    print res
