#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/15 9:52
# @Author  : zhm
# @File    : genUserInfo.py
# @Software: PyCharm
import MySQLdb


class User:
    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "1234", "fiverr")

    def process(self):

        cursor = self.db.cursor()
        sql = "SELECT rater_id,rater_username,gig_id,value,update_on FROM comment WHERE is_seller=0 order by rater_id"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            gid = str(row[2])
            sql = "SELECT duration,price,sub_category,seller_name FROM gig_property WHERE id=%s"
            cursor.execute(sql, gid)
            gig = cursor.fetchone()
            sql = "insert into user_info (user_id,rater_username,gig_id,score,update_on,duration,price,sub_category,seller_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], gig[0], gig[1], gig[2], gig[3]))
        self.db.commit()


# if __name__ == '__main__':
#     t = User()
#     t.process()