import scrapy
from ..items import StackoverflowItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy
import re
import mysql.connector


class StackSpider(scrapy.Spider):
    name = 'StackSpider'
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='programming',
    )
    curr = conn.cursor()

    def get_links(self, limit=10):
        l = []
        datas = self.where(tbl='related_answer', column='status',
                           value=0, all=True, limit=limit)

        for link in datas:
            l.append(link['link'])
            self.update(tbl='related_answer', column='status',
                        value=1, id=link['id'])
        # print(l)
        return l

    def get_formated_data(self, headers, data):
        try:
            data = dict(zip([c[0] for c in headers], data))
        except:
            data = None
        return data

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

    def update(self, tbl, column, value, id):

        sql = "UPDATE {tbl} SET `{column}` = '{value}' WHERE `id` = '{id}';".format(
            tbl=tbl, column=column, value=value, id=id)
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()
        c.close()
        return True  # c.rowcount

    def start_requests(self):
        # urls = links
        # p=ps_proxy()
        # https://gist.github.com/cydu/8a4b9855c5e21423c9c5
        for url in self.get_links(limit=1):

            # yield self.get(url=url, callback=self.parse)
            yield scrapy.Request(url=url, callback=self.parse)

    # def get(self, url, callback):
    #     r = requests.get(url=url                         # callback=self.parse,
    #                      , headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}

    #                      )
    #     callback(r)
    #     return r

    def parse(self, response):

        items = StackoverflowItem()

        links = response.css(".sidebar-related,.sidebar-linked")
        related_answers = []

        for t in links:

            # title = t.css('a.question-hyperlink').css('::text').extract()
            link = t.css('a.question-hyperlink').css('a::attr(href)').extract()
            related_answers.append(link)

        answers = []

        allanswer = response.css('[id^="answer-"]')
        # index = 0
        for a in allanswer:
            # index += 1
            # print('index : {0}'.format(index))
            codearg = []
            accept = None  # a.css('svg.iconCheckmarkLg').get()
            authors = a.css(
                '.mt24 .user-details>a')
            author_name = authors.css('::text').extract()
            author_url = authors.css('::attr(href)').extract()

            codes = a.css('pre>code')
            for c in codes:
                # c.css('::text').extract()
                codearg.append(
                    {'code': c.css('::text').get()})

            vote = a.css('.js-vote-count::attr(data-value)').get()

            json = {'codes': codearg, 'vote': vote,
                    'accept': accept, 'author_name': author_name, 'author_url': author_url}
            answers.append(json)

        items['title'] = response.css('title::text').get()
        items['url'] = response.url
        items['answer'] = answers
        items['related_answers'] = related_answers

        yield items


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings(), {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    })

    process.crawl(StackSpider)
    process.start()  # the script will block here until the crawling is finished
