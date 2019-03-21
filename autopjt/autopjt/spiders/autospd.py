# -*- coding: utf-8 -*-
import scrapy

from furl import furl
from scrapy.http import Request
from autopjt.items import AutopjtItem


class AutospdSpider(scrapy.Spider):
    name = 'autospd'
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/pg1-cid4004279.html']

    def parse(self, response):
        for _list in response.xpath('//div[@id="search_nature_rg"]/ul/li'):
            item = AutopjtItem()
            # 商品名称
            item['name']  = _list.xpath('./a/@title').extract_first()
            # 商品链接
            item['price']  = _list.xpath('./a/@href').extract_first()
            # 商品评论数
            item['comnum']  = _list.xpath('./p[@class="star"]/a/text()').extract_first().strip('条评论')
            # 商品价格
            item['link']  = _list.xpath('./p/span/text()').extract_first().strip('¥')
            yield item
            print(item['name'])
        # 判断是否有下一页
        page = response.xpath('//a[text()[contains(., "下一页")]]/@href').extract_first()
        if bool(page):
            fu = furl(response.url)
            fu_base = fu.copy().remove(path=True, args=True)
            next_page = fu_base.add(path=page).url  # 构造完整URL
            yield scrapy.Request(url=next_page, callback=self.parse)
