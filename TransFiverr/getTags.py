#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb


class Tag:
    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "1234", "fiverr")

    def process(self):
        tagToGig = {}

        cursor = self.db.cursor()
        sql = "SELECT id,tags FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            ids = str(row[0])
            tags = str(row[1]).lower().split(',')
            for each in tags:
                tagToGig.setdefault(each, []).append(ids)
                print ids + '：' + each

        sql = "insert into gigtotag (gid, tag) VALUES (%s, %s)"
        for key in tagToGig:
            for ids in tagToGig[key]:
                print sql, (ids, key)
                cursor.execute(sql, (ids, key))
        self.db.commit()


if __name__ == '__main__':
    t = Tag()
    t.process()
