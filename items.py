# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StackoverflowItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    answer = scrapy.Field()
    # link = scrapy.Field()
    related_answers = scrapy.Field()
