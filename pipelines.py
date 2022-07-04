# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from tkinter.messagebox import NO
from itemadapter import ItemAdapter

import mysql.connector


class StackoverflowPipeline:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='programming',
    )
    curr = conn.cursor()

    def save_q(self, title, url):

        sql = ("INSERT INTO questions "
               "(title, url, status) "
               "VALUES (%s,%s, %s)")

        data = (title, url, 1)
        # data = (self.title, self.site, self.location, self.price, self.housing,
        # self.extra, self.images, self.body, self.post_time, self.url)

        self.curr.execute(sql, data)
        self.conn.commit()
        # curr.close()
        return self.curr.lastrowid

    def save_link(self, url):

        sql = ("INSERT INTO related_answer "
               "(link,status)" "VALUES (%s,%s)")

        data = (url, 0)
        # data = (self.title, self.site, self.location, self.price, self.housing,
        # self.extra, self.images, self.body, self.post_time, self.url)

        self.curr.execute(sql, data)
        self.conn.commit()
        # curr.close()
        return self.curr.lastrowid

    def check_link(self, url):
        data = self.where(tbl='related_answer',
                          column='link', value=url, all=False)

        if data:
            return True
        return False

    def get_links(self):
        l = []
        datas = self.where(tbl='related_answer', column='status',
                           value=0, all=True, limit=10)
        for link in datas:
            l.append(link['link'])
            self.update(tbl='related_answer', column='status',
                        value=1, id=link['id'])
        return l

    def update(self, tbl, column, value, id):

        sql = "UPDATE {tbl} SET `{column}` = '{value}' WHERE `id` = '{id}';".format(
            tbl=tbl, column=column, value=value, id=id)
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()
        c.close()
        return True  # c.rowcount

    def where(self, tbl, column, value, all=False, limit=100):
        c = self.conn.cursor(buffered=True)
        sql = "SELECT * FROM `{tbl}` WHERE `{column}` = '{value}' LIMIT {limit};".format(
            tbl=tbl, column=column, value=value, limit=limit)

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

    def get_formated_data(self, headers, data):
        try:
            data = dict(zip([c[0] for c in headers], data))
        except:
            data = None
        return data

    def save_a(self, text=None, vote=None, accept=None, autho_name=None, author_url=None, source=None, question_id=None):
        sql = ("INSERT INTO answers "
               "(text, vote, accept,autho_name,author_url,source,question_id) "
               "VALUES (%s,%s, %s, %s, %s, %s, %s)")

        data = (text, vote, accept, autho_name,
                author_url, source, question_id)

        self.curr.execute(sql, data)
        self.conn.commit()
        # curr.close()
        return self.curr.lastrowid

    def save_code(self, answer_code, code_lang, answer_id):
        sql = ("INSERT INTO code "
               "(answer_code, code_lang, answer_id) "
               "VALUES (%s,%s, %s)")

        data = (answer_code, code_lang, answer_id)

        self.curr.execute(sql, data)
        self.conn.commit()
        # curr.close()
        return self.curr.lastrowid

    def process_item(self, item, spider):
        self.store_db(item)
        # return item['related_answers']

    def last_index(self, args):
        return len(args)-1

    def last_item(self, args):

        return args[self.last_index(args)]

    def store_db(self, item):
        qId = self.save_q(item['title'], item['url'])
        for link in item['related_answers']:

            for i in link:
                # print('https://stackoverflow.com'+i)

                if not self.check_link('https://stackoverflow.com'+i):
                    self.save_link('https://stackoverflow.com'+i)
                else:
                    pass
                    # print('url in datasess')

        for a in item['answer']:

            try:
                aId = self.save_a(text='text', question_id=qId, source='stackoverflow',
                                  vote=a['vote'], autho_name=self.last_item(a['author_name']), author_url=self.last_item(a['author_url']))
                # print('..............answer.......................')

                for c in a['codes']:

                    # print('..............code.......................')

                    self.save_code(
                        answer_code=c['code'], code_lang=None, answer_id=aId)
            except Exception as e:
                print(e)

                # print(code['code'])

            # aId = self.save_a(qId)

            # item['related_qs'][0],
            # item['vote'][0],

            # item['answer']
