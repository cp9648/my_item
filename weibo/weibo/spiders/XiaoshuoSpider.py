# -*- coding: utf-8 -*-
import scrapy
# from xiaoshuo.items import XiaoshuoItem


class XiaoshuospiderSpider(scrapy.Spider):
    name = 'XiaoshuoSpider'
    allowed_domains = ['www.xbiquge.la']
    start_urls = ['http://www.xbiquge.la//']

    def parse(self, response):
        book_name_url = response.xpath('//li/a[contains(text(),"神记")]/@href').extract_first()
        yield scrapy.Request(url=book_name_url, callback=self.parse_zhangjie)

    def parse_zhangjie(self, response):
        '''进入一本书的章节页面'''
        zhangjie_url = response.xpath('//*[@id="list"]/dl/dd[1]/a/@href').extract_first()
        _url = 'http://www.xbiquge.la{}'.format(zhangjie_url)
        yield scrapy.Request(url=_url, callback=self.parse_content)

    def parse_content(self, response):
        url = response.url
        # item = XiaoshuoItem()
        item = {}
        item['title'] = response.xpath('//div[@id="wrapper"]/div[4]/div/div[2]/h1/text()').extract_first()
        item['content'] = response.xpath('//div[@id="content"]/text()').extract()
        # yield item
        print(item)

