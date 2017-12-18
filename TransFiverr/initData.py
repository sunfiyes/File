#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb


class SqlUtil:
    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "1234", "fiverr")
        self.fpath = 'D:/code_py/TransFiverr/data/'

    def exportEntity(self):
        res = []
        cursor = self.db.cursor()

        # 导出gig
        sql = "SELECT id FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            ids = str(row[0])
            res.append('/gig/' + ids + '\t' + ids + '\n')

        # 导出seller
        sql = "SELECT DISTINCT seller_name FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            ids = str(row[0])
            res.append('/seller/' + ids + '\t' + ids + '\n')

        # 导出customer
        sql = "SELECT DISTINCT rater_username FROM comment WHERE is_seller=0"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            ids = str(row[0])
            res.append('/customer/' + ids + '\t' + ids + '\n')

        # 导出category
        sql = "SELECT DISTINCT category FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            ids = str(row[0])
            res.append('/category/' + ids + '\t' + ids + '\n')

        # 导出subcategory
        sql = "SELECT DISTINCT sub_category FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            ids = str(row[0])
            res.append('/subcategory/' + ids + '\t' + ids + '\n')

        # 导出tag
        sql = "SELECT DISTINCT tag FROM gigtotag"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            tag = str(row[0])
            res.append('/tag/' + tag + '\t' + tag + '\n')

        # 导出duration
        sql = "SELECT DISTINCT duration FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            duration = str(row[0])
            res.append('/duration/' + duration + '\t' + duration + '\n')

        # 导出price
        sql = "SELECT DISTINCT price FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            price = str(row[0])
            res.append('/price/' + price + '\t' + price + '\n')


        with open(self.fpath + 'entity2id.txt', 'w') as fo:
            fo.writelines(res)

    def exportRelation(self):
        res = []
        res.append('_buy' + '\t' + '1\n')
        res.append('_provide' + '\t' + '2\n')
        res.append('_belong' + '\t' + '3\n')
        res.append('_sub_belong' + '\t' + '4\n')
        res.append('_has_tag' + '\t' + '5\n')
        res.append('_price' + '\t' + '6\n')
        res.append('_duration' + '\t' + '7\n')
        with open(self.fpath + 'relation2id.txt', 'w') as fo:
            fo.writelines(res)

    def exportTriple(self):
        res = []
        cursor = self.db.cursor()

        # _buy
        sql = "SELECT DISTINCT rater_username,gig_id FROM user_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            uid = str(row[0])
            gid = str(row[1])
            res.append('/customer/' + uid + '\t' + '/gig/' + gid + '\t' + '_buy' + '\n')

        # _provide
        sql = "SELECT DISTINCT seller_name,id FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            uid = str(row[0])
            gid = str(row[1])
            res.append('/seller/' + uid + '\t' + '/gig/' + gid + '\t' + '_provide' + '\n')

        # _belong
        sql = "SELECT DISTINCT sub_category,category FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            s = str(row[0])
            g = str(row[1])
            res.append('/subcategory/' + s + '\t' + '/category/' + g + '\t' + '_belong' + '\n')

        # _sub_belong
        sql = "SELECT DISTINCT id,sub_category FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            gid = str(row[0])
            cate = str(row[1])
            res.append('/gig/' + gid + '\t' + '/subcategory/' + cate + '\t' + '_sub_belong' + '\n')

        # _has_tag
        sql = "SELECT DISTINCT gid,tag FROM gigtotag"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            gid = str(row[0])
            tag = str(row[1])
            res.append('/gig/' + gid + '\t' + '/tag/' + tag + '\t' + '_has_tag' + '\n')

        # _price
        sql = "SELECT DISTINCT id,price FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            uid = str(row[0])
            gid = str(row[1])
            res.append('/gig/' + uid + '\t' + '/price/' + gid + '\t' + '_price' + '\n')

        # _duration
        sql = "SELECT DISTINCT id,duration FROM gig_property"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            uid = str(row[0])
            gid = str(row[1])
            res.append('/gig/' + uid + '\t' + '/duration/' + gid + '\t' + '_duration' + '\n')


        with open(self.fpath + 'train.txt', 'w') as fo:
            fo.writelines(res)


if __name__ == '__main__':
    sqlutil = SqlUtil()
    sqlutil.exportEntity()
    sqlutil.exportRelation()
    sqlutil.exportTriple()
