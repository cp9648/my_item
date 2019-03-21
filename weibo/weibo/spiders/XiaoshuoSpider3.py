# -*- coding: utf-8 -*-
import scrapy
# from xiaoshuo.items import XiaoshuoItem
from weibo.items import WeiboItem


class XiaoshuospiderSpider(scrapy.Spider):
    name = 'XiaoshuoSpider3'
    allowed_domains = ['www.xbiquge.la']
    start_urls = ['http://www.xbiquge.la/']

    def parse(self, response):
        print(response.url)
        book_name_url = response.xpath('//li/a[contains(text(),"神记")]/@href').extract_first()
        print(book_name_url)
        yield scrapy.Request(url=book_name_url, callback=self.parse_zhangjie)

    def parse_zhangjie(self, response):
        '''进入一本书的章节页面'''
        zhangjie_url = response.xpath('//div[@id="list"]/dl/dd/a/@href').extract()
        for zhangjie in zhangjie_url:
            _url = 'http://www.xbiquge.la{}'.format(zhangjie)
            yield scrapy.Request(url=_url, callback=self.parse_content)

    def parse_content(self, response):
        # item = XiaoshuoItem()
        item = WeiboItem()
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        item['content'] = response.xpath('//div[@id="content"]/text()').extract()
        nextpage = response.xpath('//div/a[contains(text(),"下一章")]/@href').extract_first()
        yield item
        print(item['title'])

