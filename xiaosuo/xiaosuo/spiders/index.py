# -*- coding: utf-8 -*-
import scrapy
import json
import os
import urllib
import time

from scrapy.http import Request
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
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-plugins-discovery")
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
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
    print(existed)
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


class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['doupocangqiong1.com']
    start_urls = ['https://doupocangqiong1.com/1/1.html']

    def parse(self, response):
        # import ipdb; ipdb.set_trace()
        driver_path = self.settings.get('DRIVER_PATH')
        browser = gen_browser(driver_path)
        # time.sleep(1)
        browser.get(response.url)  # 打开页面

        name = browser.find_element_by_xpath('/html/body/section/div/article[1]/div[1]/div/span[1]/a').text
        zan = browser.find_element_by_xpath('/html/body/section/div/article[1]/div[1]/h1/a').text
        value = browser.find_element_by_xpath('//*[@id="chaptercontent"]').text
        print(name)
        print(zan)
        print(value)
        # name = response.xpath('/html/body/section/div/article[1]/div[1]/div/span[1]/a/text()').extract_first()
        # zan = response.xpath('/html/body/section/div/article[1]/div[1]/h1/a/text()').extract_first().strip(name + ' ')
        # value = response.xpath('//*[@id="chaptercontent"]/text()')
