#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/15 9:52
# @Author  : zhm
# @File    : genUserInfo.py
# @Software: PyCharm
from collections import defaultdict

import MySQLdb


class UserAnalysis:
    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "1234", "fiverr")

    def process(self, user_name):

        cursor = self.db.cursor()
        sql = "SELECT user_id,rater_username,gig_id,score,update_on,duration,price,sub_category,seller_name FROM user_info WHERE rater_username=%s"
        cursor.execute(sql, user_name)
        result = cursor.fetchall()
        dic = defaultdict(int)
        for row in result:
            key = 'duration/'+str(row[5])
            dic[key] += 1
            key = 'price/'+str(row[6])
            dic[key] += 1
            key = 'sub_category/'+str(row[7])
            dic[key] += 1
            key = 'seller_name/'+str(row[8])
            dic[key] += 1
        s_list = sorted(dic.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        print s_list
        return s_list[:3]
ua = UserAnalysis()
if __name__ == '__main__':
    t = UserAnalysis()
    t.process('jea22jea22')
