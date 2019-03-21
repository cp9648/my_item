# -*- coding: utf-8 -*-
import scrapy
from demo.items import DemoItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/114134/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        article_urls = response.xpath('//a[@class="archive-title"]/@href').extract()
        print('*' * 60)
        for url in article_urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath('//*[@id="archive"]/div[21]/a[4]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_time = response.xpath('//div[@class="entry-meta"]/p/text()').extract_first().lstrip().rstrip(' ·')
        content = response.xpath('//div[@class="entry"]').extract_first()
        url = response.url

        item = DemoItem()
        item['title'] = title
        item['create_time'] = create_time
        item['content'] = content
        item['url'] = url
        yield item
