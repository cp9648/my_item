# -*- coding: utf-8 -*-
import scrapy
import re

from furl import furl
from zhaopin.items import ZhaopinItem


class ZpSpider(scrapy.Spider):
    name = 'zp'
    allowed_domains = ['www.bjzph.com']
    start_urls = ['https://www.bjzph.com/']

    def parse(self, response):
        # 链接黑名单
        path_blask_list = ['zhaopinqiye', 'beijingguozhanzhaopinhui']
        links = response.xpath('//ul/li/a/@href').extract()
        print(links)
        
        for url in links:
            # 取出path
            fu = furl(response.url)
            fu_base = fu.copy().remove(path=True, args=True)
            path = str(fu.path).strip('/')
            # 2.判断当前url路径是否在黑名单里
            if path.split('/')[0] in path_blask_list:
                return None
            # 3、URl 补充完整
            # import ipdb as pdb; pdb.set_trace()
            furl_url = fu_base.set(path=url).url
            callback_func = self.parse  # 默认当前页面解析
            # 如果URl规则符合详细页面规则
            if re.search(r'\d+\/\d', furl_url):
                # 采用详细页面解析发
                callback_func = self.parse_detail
            
            yield scrapy.Request(url=furl_url, callback=callback_func)
        # 判断是否有下一页
        next_page = response.xpath('//a[text()[contains(., "下一页")]]/@href').extract()
        print(next_page, '*' * 60)
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = ZhaopinItem()
        # 主题
        item['title'] = response.xpath('//div[@class="title"]/text()').extract_first()
        # 内容链接
        item['url'] = response.url
        # 开始时间
        item['starttime'] = response.xpath('//div[@class="starttime"]/text()').extract_first()
        # 结束时间
        item['endtime'] = response.xpath('//div[@class="endtime"]/text()').extract_first()
        # 招聘城市
        item['cityname'] = response.xpath('//div[@class="cityname"]/text()').extract_first()
        # 详细地址
        item['address'] = response.xpath('//div[@class="address"]/text()').extract_first()
        # 详细内容
        item['content'] = response.xpath('//div[@class="middleLeft"]/p[1]/text()').extract_first()
        # import ipdb as pdb; pdb.set_trace()

        yield item
        