# -*- coding: utf-8 -*-
import scrapy
import json

from furl import furl
from Jobs.items import JobsItem


class Job51spiderSpider(scrapy.Spider):
    name = 'Job51Spider'
    allowed_domains = ['www.51job.com', 'js.51jobcdn.com', 'search.51job.com']
    start_urls = ['https://www.51job.com/']
    _url = r'https://search.51job.com/list/{0},000000,0000,00,9,99,{1},2,1.html'
    allowed_cities = ['重庆']  #, '成都', '上海', '深圳', '昆明', '杭州', '贵阳', '宁波']  ## 允许的城市

    def parse(self, response):
        # 调用获取所有城市信息
        js_url = 'https://js.51jobcdn.com/in/js/2016/layer/area_array_c.js'
        yield scrapy.http.Request(url=js_url, callback=self.parse_city, dont_filter=False)

    def parse_city(self, response):
        # encoding = chardet.detect(response.body)['encoding']
        s1 = response.body.decode('GBK', 'jglo')  # Unicode，decode(解码)需要注明当前编码格式
        data = s1.split('area=')[-1].strip(';')
        # 获取城市名及编号
        data = json.loads(data)
        for city_id in data:
            if data[city_id] in self.allowed_cities:
                # 启动 爬取某个城市 第一个请求
                yield scrapy.Request(url=self._url.format(city_id, 'python'), callback=self.parse_yei)

    def parse_yei(self, response):
        _list = response.xpath('//div[@class="dw_table"]/div[@class="el"]')
        for li in _list:
            item = JobsItem()
            # import ipdb; ipdb.set_trace()
            # 职位名称
            item['name'] = li.xpath('./p/span/a/text()').extract_first().strip()
            # 详细链接
            item['detailed_url'] = li.xpath('./p/span/a/@href').extract_first().strip()
            # 公司名称
            item['company_name'] = li.xpath('./span[@class="t2"]/a/text()').extract_first().strip()
            # 公司链接
            item['company_url'] = li.xpath('./span[@class="t2"]/a/@href').extract_first().strip()
            # 工作地址
            item['Work_address'] = li.xpath('./span[@class="t3"]/text()').extract_first().strip()
            # 薪资
            item['salary'] = li.xpath('./span[@class="t3"]/text()').extract_first().strip()
            # 发布时间
            item['time'] = li.xpath('./span[@class="t3"]/text()').extract_first().strip()
            yield item
        yei = response.xpath('//li[@class="bk"][2]/a/@href').extract_first()
        if bool(yei):
            yield scrapy.Request(url=yei, callback=self.parse_yei)
