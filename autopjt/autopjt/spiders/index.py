# -*- coding: utf-8 -*-
import scrapy
import json


class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['product.dangdang.com']
    start_urls = ['http://product.dangdang.com/1463252947.html']

    def parse(self, response):
        with open('data.json', 'r', encoding='utf-8') as f:
            for _list in json.load(f):
                print(_list['price'])
