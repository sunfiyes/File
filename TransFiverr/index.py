#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
import sys
import json
import MySQLdb
from copy import deepcopy
from numpy import *
from flask import Flask
from flask import send_file
from flask import request

from UserAnalysis import UserAnalysis

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.debug = True

INDEX = {'duration': 3, 'price': 4, 'sub_category': 5, 'seller': 6, }
Q_LIST = []

@app.route('/')
def home():
    return send_file('D:/code_py/TransFiverr/index.html')


@app.route('/reco')
def ars():
    global Q_LIST
    query = request.args.get('query').lower()
    SEL = json.loads(request.args.get('sel'))
    # print SEL
    # tags = ['php', 'cms', 'website', 'responsive', 'build website']
    tags = q.extractTags(query)
    sortList = q.queryByTag(tags)
    i = 0
    for qa in Q_LIST:
        if SEL[i] == 1:
            sortList = q.getSpecify(qa, sortList)
        i += 1
    res = q.getDetail(sortList)
    res.append(tags)
    return json.dumps(res)

@app.route('/choice')
def choice():
    global Q_LIST
    res = []
    username = request.args.get('username')
    ua = UserAnalysis()
    Q_LIST = ua.process(username)
    for qa in Q_LIST:
        key = qa[0].split('/', 1)[0]
        val = qa[0].split('/', 1)[1]
        res.append((key, val))
    return json.dumps(res)


class QueryUtil:
    def __init__(self):
        dbpath = 'D:/code_py/TransFiverr/data/bak/'
        self.entityDic = self.loadData(dbpath + 'entityVector.txt')
        self.relationDic = self.loadData(dbpath + 'relationVector.txt')
        self.tagDic = self.loadTagDic()

    def loadData(self, str):
        fr = open(str)
        sArr = [line.strip().split("\t") for line in fr.readlines()]
        datArr = [[float(s) for s in line[1][1:-1].split(", ")] for line in sArr]
        nameArr = [line[0] for line in sArr]
        dic = {}
        for name, vec in zip(nameArr, datArr):
            dic[name] = array(vec)
        return dic

    def loadTagDic(self):
        db = MySQLdb.connect("localhost", "root", "1234", "fiverr")
        res = []
        cursor = db.cursor()
        sql = "SELECT DISTINCT tag FROM gigtotag ORDER BY CHAR_LENGTH(tag)"
        cursor.execute(sql)
        dset = cursor.fetchall()
        for row in dset:
            res.append(row[0])
        return res

    def queryByTag(self, tagList):
        entityDic = self.entityDic
        relaVec = self.relationDic['_has_tag']
        res = {}
        for entity in entityDic:
            if entity.startswith('/gig'):  # 只遍历gig
                loss = 0
                for tag in tagList:
                    tag = '/tag/' + tag
                    loss += linalg.norm(entityDic[entity] + relaVec - entityDic[tag])
                res.setdefault(entity, loss/len(tagList))
        sortList = sorted(res.items(), lambda x, y: cmp(x[1], y[1]))
        return sortList[0:100]

    def getDetail(self, sortList):
        # 打开数据库连接
        db = MySQLdb.connect("localhost", "root", "1234", "fiverr")
        res = []
        cnt = 0
        cursor = db.cursor()
        sql = "SELECT id,title,duration,price,seller_name,sub_category,category,description FROM gig_property WHERE id=%s"
        for gig in sortList:
            gid = gig[0][5:]
            cursor.execute(sql, gid)
            row = cursor.fetchone()
            tmp = [unicode(str(s), errors='ignore') for s in row]
            tmp.append(str(gig[1]))
            res.append(tmp)
            cnt += 1
        db.close()
        return res

    def getSpecify(self, query, sortList):
        # 打开数据库连接
        key = query[0].split('/', 1)[0]
        val = query[0].split('/', 1)[1]
        db = MySQLdb.connect("localhost", "root", "1234", "fiverr")
        res = []
        s_list = []
        cursor = db.cursor()
        sql = "SELECT id FROM gig_property WHERE id=%s AND "+key+"=%s"
        for gig in sortList:
            gid = gig[0][5:]
            cursor.execute(sql, (gid, val))
            row = cursor.fetchone()
            if row:
                tmp = [unicode(str(s), errors='ignore') for s in row]
                tmp.append(str(gig[1]))
                res.append(tmp)
                s_list.append(gig)
        db.close()
        return s_list

    def extractTags(self, query):
        res = []
        for tag in self.tagDic:
            if tag in query:
                res.append(tag)
        return res


if __name__ == '__main__':
    q = QueryUtil()
    app.run()
