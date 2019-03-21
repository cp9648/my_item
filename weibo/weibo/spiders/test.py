# -*- coding: utf-8 -*-
import scrapy
import json
import time
import os

from furl import furl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    StaleElementReferenceException
)

def gen_browser(driver_path):
    '''实例化一个driver'''
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--load-images=false")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-plugins-discovery")
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    options.add_argument('user-agent="{0}"'.format(user_agent))
    # ############### 专业造假 ***************************

    def send(driver, cmd, params={}):
        '''
        向调试工具发送指令
        from: https://stackoverflow.com/questions/47297877/to-set-mutationobserver-how-to-inject-javascript-before-page-loading-using-sele/47298910#47298910
        '''
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        if response['status']:
            raise Exception(response.get('value'))
        return response.get('value')

    def add_script(driver, script):
        '''在页面加载前执行js'''
        send(driver, "Page.addScriptToEvaluateOnNewDocument", {"source": script})
    # 给 webdriver.Chrome 添加一个名为 add_script 的方法
    webdriver.Chrome.add_script = add_script  # 这里（webdriver.Chrome）可能需要改，当调用不同的驱动时
    # *************** 专业造假 ###################
    browser = webdriver.Chrome(
        executable_path=driver_path,
        chrome_options=options
    )
    # ################## 辅助调试 *********************
    existed = {
        'executor_url': browser.command_executor._url,  # 浏览器可被远程连接调用的地址
        'session_id': browser.session_id  # 浏览器会话ID
    }
    # print(existed)
    # ********************* 辅助调试 ##################
    # ############### 专业造假 ***************************
    browser.add_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
    });
    window.navigator.chrome = {
        runtime: {},
    };
    Object.defineProperty(navigator, 'languages', {
        get: () => ['zh-CN', 'zh']
    });
    Object.defineProperty(navigator, 'plugins', {
        get: () => [0, 1, 2],
    });
    """)
    # *************** 专业造假 ###################
    return browser

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['https://m.weibo.cn/profile/2677042071']

    def parse(self, response):
        driver_path = self.settings.get('DRIVER_PATH')
        browser = gen_browser(driver_path)
        browser.get(response.url)  # 打开页面
        browser.find_element_by_xpath('//span[@class="prf-num"][1]').click()  # 模拟点击关注
        time.sleep(2)
        # 获取点击自后的页面url
        _url = browser.current_url
        # 判断网页是否跳转
        if _url == response.url:
            time.sleep(3)
            _url = browser.current_url
        yield scrapy.Request(url=_url, callback=self.parse_attention)

    def parse_attention(self, response):
        print(response.url)
        import ipdb; ipdb.set_trace()
        f = furl(response.url)
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
