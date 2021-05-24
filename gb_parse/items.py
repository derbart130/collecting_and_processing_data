# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramTagItem(scrapy.Item):
    data_parse = scrapy.Field()
    data = scrapy.Field()


class InstagramPostItem(scrapy.Item):
    data_parse = scrapy.Field()
    data = scrapy.Field()
