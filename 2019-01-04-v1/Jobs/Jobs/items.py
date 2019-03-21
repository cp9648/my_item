# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名称
    name = scrapy.Field()
    # 详细链接
    detailed_url = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 公司链接
    company_url = scrapy.Field()
    # 工作地址
    Work_address = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
