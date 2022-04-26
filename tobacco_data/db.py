#!/usr/bin/env python

# -*- encoding: utf-8 -*-
import pymysql
import logging

from tobacco_data.items import product
from tobacco_data.spiders import brand


class DB_MySQL():
    '''数据库操作类'''
    HOST = '123.57.165.135'
    PORT = 50007
    USER = 'xyh'
    PASSWD = 'HUjy0b3L4&yu'
    DBNAME = 'cigarette_info_temp'
    CHARSET = 'utf8'

    def __init__(self):
        self.conn = pymysql.connect(host=self.HOST, port=int(self.PORT), user=self.USER, passwd=self.PASSWD,
                                    db=self.DBNAME, charset=self.CHARSET)
        self.cur = self.conn.cursor()

    # # 插入数据
    # def insert(self, item):

    # 判断url是否已经存在
    def url_is_exist(self, url):
        try:
            if "Product" in url:
                if self.cur.execute('select * from product where URL = %s limit 1', (url,)):
                    return True
                else:
                    return False
            if self.cur.execute('select * from yanyue where URL = %s limit 1', (url,)):
                return True
            if ".jpg" or ".png" in url:
                print(1111111)
                if self.cur.execute('select * from image where URL = %s limit 1', (url,)):
                    return True
                else:
                    return False
            else:
                return False

        except Exception as e:
            logging.error('mysql查询origin_url是否存在执行异常: ' + str(e))

    def close(self):
        self.cur.close()
        self.conn.close()


db_mysql = DB_MySQL()
