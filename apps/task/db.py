# -*- coding: utf-8 -*-

"""

Save data to MySQL

"""
try:
    import MySQLdb
    from MySQLdb import MySQLError
except ImportError:
    MySQLdb = None
import time
import re

class DBAdapter:
    def db_connect(self):
        conn = MySQLdb.connect(host="172.19.160.185",port=3306,db="easyapi",user="tcredit_tester",passwd="tcredit0401",charset="utf8")
        return conn

    def ext(self,sql,k=None):
        conn = self.db_connect()
        cur = conn.cursor()
        if k :
            cur.execute(sql,k)
        else :
            cur.execute(sql)
        data = cur.fetchall()
        # print str(data[0])+'   '+str(len(data))
        cur.close()
        conn.commit()
        conn.close()
        return data

    def update(self,sql,k=None):
        conn = self.db_connect()
        cur = conn.cursor()
        if k :
            cur.execute(sql,k)
        else :
            cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
        return