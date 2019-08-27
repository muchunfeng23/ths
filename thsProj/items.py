# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThsprojItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    pass

class ShareEveryDayItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    pass

class DataItem(scrapy.Item):
    content = scrapy.Field()
    pass


class ConceptFromThsItem(scrapy.Item):
    content = scrapy.Field()
    pass
