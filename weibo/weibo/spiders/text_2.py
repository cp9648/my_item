# -*- coding: utf-8 -*-
import scrapy
import json
import time
import os

from furl import furl
from weibo.items import WeiboItem


class Text2Spider(scrapy.Spider):
    name = 'text_2'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['https://m.weibo.cn/profile/info?uid=3083675110']
    custom_settings = {
            'LOG_LEVEL': 'DEBUG',
            'LOG_FILE': '5688_log_%s.txt' % time.time(),  # 配置的日志
            "DEFAULT_REQUEST_HEADERS": {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            }
        }  # 添加的请求头

    # 最近消息页面（包含关注量粉丝量）
    message = furl('https://m.weibo.cn/profile/info?uid=3083675110')
    # 全部博文页面
    bowen = furl('https://m.weibo.cn/api/container/getIndex?containerid=2304133083675110_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=1')
    # 我的关注页面
    attention = furl('https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_3083675110&page=1')
    # 我的粉丝页面
    fans = furl('https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_3083675110&since_id=1')
    data = set()

    def parse(self, response):
        # 保存结果
        item = WeiboItem()
        resp_dict = json.loads(response.body_as_unicode())
        user = resp_dict['data']['user']
        # 用户id
        item['uid'] = user['id']
        # 用户名
        item['screen_name'] = user['screen_name']
        # 博文主页
        item['profile_url'] = user['profile_url']
        # 关注量
        item['follow_count'] = user['follow_count']
        # 粉丝
        item['followers_count'] = user['followers_count']
        print(user['screen_name'])
        yield item

        # 用户id
        uid = furl(response.url).args['uid']
        # 修改为当前用户id
        self.attention.args['containerid'] = '231051_-_followers_-_{}'.format(uid)
        if uid not in self.data:
            self.data.add(uid)
            yield scrapy.Request(url=self.attention.url, meta={'uid': uid}, callback=self.parse_follow)
        

    def parse_follow(self, response):
        resp_dict = json.loads(response.body_as_unicode())
        if resp_dict['ok'] == 1:
            # 获取用户列表
            card_group = resp_dict['data']['cards'][-1]['card_group']
            for card in card_group:
                # 获取用户ID
                uid = card['user']['id']
                self.message.args['uid']=uid
                if uid not in self.data:
                    yield scrapy.Request(url=self.message.url, callback=self.parse)
            # import ipdb; ipdb.set_trace()
            self.attention.args['page'] = int(self.attention.args['page'])+1
            yield scrapy.Request(url=self.attention.url, meta={'uid': response.url}, callback=self.parse_follow)

    # def parse_attention(self, response):
        # import ipdb; ipdb.set_trace()


        # 'https://m.weibo.cn/profile/2677042071'
        # 'https://m.weibo.cn/p/index?containerid=231051_-_followers_-_2677042071'
        # 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_2677042071&page=2'
        # yield scrapy.http.Request(url=f, callback=self.parse_attention)
        # '231051_-_followers_-_'
        # path_cont = f.args['containerid']  # '231051_-_followers_-_2677042071'
        # f.remove(path=True).join('api/container/getIndex')
        # f.args['containerid'] = path_cont
        # f.args['page'] = '2'
        # https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_2677042071&page=2
        # 'https://m.weibo.cn/p/index?containerid=231051_-_followerstagrecomm_-_3083675110_-_1042015%3AtagCategory_012&luicode=10000011&lfid=231051_-_followers_-_3083675110'

        # 我的id = 3083675110
        
        # 最近消息页面（包含关注量粉丝量）
        # 'https://m.weibo.cn/profile/info?uid=3083675110'

        # 全部博文页面（第二页）
        # https://m.weibo.cn/api/container/getIndex?containerid=2304133083675110_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=2

        # 我的关注页面（第二页）
        # https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_3083675110&page=2

        # 我的粉丝页面（第二页）
        # https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_3083675110&since_id=2
