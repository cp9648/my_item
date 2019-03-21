# -*- coding: utf-8 -*-
import re
import redis
import scrapy

from furl import furl
from bjzph.items import BjzphItem


class BjzphCqSpider(scrapy.Spider):
    name = 'bjzph_cq'
    allowed_domains = ['www.bjzph.com']
    start_urls = ['http://www.bjzph.com/']
    clinet = redis.Redis(decode_responses=True)

    def parse(self, response):
        # import ipdb as pdb; pdb.set_trace()
        # 链接路径黑名单
        # 1. 取出path
        fu = furl(response.url)
        fu_base = fu.copy().remove(path=True, args=True)
        path = str(fu.path).strip('/')
        # 2. 判断当前url路径是否在黑名单里
        if self.clinet.set(path.split('/')[0]):
            return None

        # 所有的链接
        links = response.xpath('//ul/li/a/@href').extract()
        for url in links:
            # 3. URL补充完整
            full_url = fu_base.set(path=url).url
            callback_func = self.parse  # 默认当做列表页面解析
            # 如果URL规则符合详细页面规则
            # import ipdb as pdb; pdb.set_trace()
            if re.search(r'\d+\/\d+', full_url):
                # 采用详细页面解析方法
                callback_func = self.parse_detail
            yield scrapy.Request(url=full_url, callback=callback_func)
        
        # 处理"下一页"
        next_page = response.xpath('//*[text()[contains(.,"下一页")]]/@href').extract_first()
        if bool(next_page):
            next_page = fu.copy().add(path=next_page).url  # 构造完整URL
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        # import ipdb as pdb; pdb.set_trace()
        fu = furl(response.url)
        path = str(fu.path).strip('/')
        # 2. 判断当前url路径是否在黑名单里
        if self.clinet.set(path.split('/')[0]):
            return None
        try:
            item = BjzphItem()
            item['name'] = response.xpath('//div[@class="title"]/text()').extract_first()
            item['url'] = response.url
            item['start_time'] = response.xpath('//div[@class="starttime"]/text()').extract_first()
            item['start_time'] = item['start_time'].split('： ')[-1]
            item['end_time'] = response.xpath('//div[@class="endtime"]/text()').extract_first()
            item['end_time'] = item['end_time'].split('： ')[-1]
            item['city'] = response.xpath('//div[@class="cityname"]/text()').extract_first()
            item['city'] = item['city'].split('： ')[-1]
            item['address'] = response.xpath('//div[@class="address"]/text()').extract_first()
            item['address'] = item['address'].split('： ')[-1]
            item['content'] = response.xpath('//div[@class="middleLeft"]/p[1]/text()').extract_first()
            # import ipdb as pdb; pdb.set_trace()
        except AttributeError as ex:
            '''
            # 取出URL前缀黑名单
            black_list = []
            item = str(furl(response.url).path).strip('/').split('/')[0]
            black_list.append(item)
            black_list = list(set(black_list))
            '''
            item = str(furl(response.url).path).strip('/').split('/')[0]
            self.clinet.get(item)
            # with open('error.txt', 'at', encoding='utf-8') as f:
            #     f.write(response.url)
            #     f.write('\n')
        yield item
