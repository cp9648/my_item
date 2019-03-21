# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    starttime = scrapy.Field()
    endtime = scrapy.Field()
    cityname = scrapy.Field()
    address = scrapy.Field()
    content = scrapy.Field()
