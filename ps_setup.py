import mysql.connector
import random
import string
import requests
import os
import time
from datetime import datetime


class table:
    def __init__(self):

        self.config = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'database': 'cldata',
            'raise_on_warnings': True
        }
        self.conn = mysql.connector.connect(**self.config)
        # print('conetion open')

    def __del__(self):
        # print('conetion close')
        self.conn.close()

    def save(self, cols, velues):
        # sql = "INSERT INTO '{0}' {1} VALUES {2};".format(tbl,cols,velus)
        # print(sql)

        c = self.conn.cursor()
        c.execute(cols, velues)
        self.conn.commit()
        c.close()
        return c.lastrowid

    def proxy_insert(self, host, port, user='no', password='no', type='no'):

        c = self.conn.cursor()
        c.execute("INSERT INTO `proxy` (`host`, `port`, `user`, `password`, `type`) VALUES ('{0}', '{1}', '{2}', '{3}', '{0}');".format(
            host, port, user, password, type))
        self.conn.commit()
        c.close()
        return c.lastrowid

    def update(self, tbl, column, value, id):

        sql = "UPDATE {tbl} SET `{column}` = '{value}' WHERE `id` = '{id}';".format(
            tbl=tbl, column=column, value=value, id=id)
        # print(sql)
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()
        c.close()
        return True  # c.rowcount

    def proxy_first(self, host, port):
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM `proxy` WHERE `host` = '{0}' AND `port` = '{1}'".format(host, port))
        proxy = c.fetchone()
        # proxy= c.fetchall()
        data = self.get_formated_data(c.description, proxy)
        c.close()
        return data

    def where(self, tbl, column, value, all=False):
        c = self.conn.cursor()
        sql = "SELECT * FROM `{tbl}` WHERE `{column}` = '{value}';".format(
            tbl=tbl, column=column, value=value)

        c.execute(sql)
        if all:
            arg = []
            data = c.fetchall()
            for p in data:
                arg.append(self.get_formated_data(c.description, p))
        else:
            data = c.fetchone()
            arg = self.get_formated_data(c.description, data)
        c.close()
        return arg

    def orderBy(self, tbl, column, value, all=False):
        c = self.conn.cursor(buffered=True)
        sql = "SELECT * FROM `{tbl}` ORDER BY `{column}` {value};".format(
            tbl=tbl, column=column, value=value)

        c.execute(sql)
        if all:
            arg = []
            data = c.fetchall()
            for p in data:
                arg.append(self.get_formated_data(c.description, p))
        else:
            data = c.fetchone()
            arg = self.get_formated_data(c.description, data)
        c.close()
        return arg

    def whereIn(self, tbl, column, value, all=False):
        c = self.conn.cursor()
        sql = "SELECT * FROM `{tbl}` WHERE `{column}` IN ('{value}');".format(
            tbl=tbl, column=column, value=value)
        # print('sql')
        # print(sql)

        c.execute(sql)
        if all:
            arg = []
            data = c.fetchall()
            for p in data:
                arg.append(self.get_formated_data(c.description, p))
        else:
            data = c.fetchone()
            arg = self.get_formated_data(c.description, data)
        c.close()
        return arg

    def proxy_all(self):
        temp = []
        proxylist = []

        c = self.conn.cursor()
        c.execute("SELECT * FROM `proxy` ORDER BY RAND() LIMIT 10")
        # proxy= c.fetchone()
        proxy = c.fetchall()

        for p in proxy:
            proxylist.append(self.get_formated_data(c.description, p))
        c.close()
        return proxylist

    def delete(self, tbl, id):
        retundata = False
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM `{0}` WHERE `id`={1}".format(tbl, id))
            self.conn.commit()
            c.close()
            retundata = True

        except Exception as e:
            print(e)
            retundata = False
        return retundata

    def time_diff(self, start, end):

        FMT = '%Y-%m-%d'
        tdelta = datetime.strptime(start, FMT) - datetime.strptime(end, FMT)
        return tdelta.days

    def time_diff_seconds(self, start, end):

        FMT = '%Y-%m-%d %H:%M:%S'
        tdelta = datetime.strptime(start, FMT) - datetime.strptime(end, FMT)
        return tdelta.seconds

    def get_formated_data(self, headers, data):
        try:
            data = dict(zip([c[0] for c in headers], data))
        except:
            data = None
        return data

    def randomString(self, stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase

        return ''.join(random.choice(letters) for i in range(stringLength))
