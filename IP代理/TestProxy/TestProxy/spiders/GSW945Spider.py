# -*- coding: utf-8 -*-
import scrapy


class Gsw945spiderSpider(scrapy.Spider):
    name = 'GSW945Spider'
    allowed_domains = ['www.gsw945.com']
    # start_urls = ['https://www.gsw945.com/']
    start_urls = ['https://httpbin.org/ip']

    def parse(self, response):
        # import ipdb; ipdb.set_trace()
        print('代理后-本机IP:')
        print(response.body_as_unicode())
        print('代理前-本机IP:')
        import requests
        print(requests.get(self.start_urls[0]).text)

# 1431322930