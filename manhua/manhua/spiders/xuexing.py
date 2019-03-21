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


class XuexingSpider(scrapy.Spider):
    name = 'xuexing'
    allowed_domains = ['www.manhuatai.com']
    start_urls = ['https://www.manhuatai.com/wudongqiankun/44.html']

    def parse(self, response):
        driver_path = self.settings.get('DRIVER_PATH')
        import ipdb; ipdb.set_trace()
        browser = gen_browser(driver_path)
        time.sleep(1)
        try:
            browser.get(response.url)  # 打开页面
        except Exception as e:
            time.sleep(5)
            browser.get(response.url)
            # import ipdb; ipdb.set_trace()

        # 获取漫画名
        name = browser.find_element_by_xpath('//div[@class="mh_wrap"]/a[2]').text
        if not os.path.exists(name):
            os.mkdir(name)
        # 获取当前章节名
        # import ipdb; ipdb.set_trace()
        van = browser.find_element_by_xpath('//div[@class="mh_readtitle"]/h1/strong').text
        os.mkdir('{}/{}'.format(name, van))
        m = 0
        for yei in range(1, len(browser.find_elements_by_xpath('//div[@class="mh_headpager"]/select[1]/option')) + 1):
            time.sleep(0.5)
            browser.find_element_by_xpath('//div[@class="mh_footpager"]/select[1]').click()
            time.sleep(0.5)
            print(yei)
            try:
                browser.find_element_by_xpath('//div[@class="mh_headpager"]/select[1]/option[{0}]'.format(yei)).click()
            except Exception as e:
                time.sleep(1)
                browser.find_element_by_xpath('//div[@class="mh_headpager"]/select[1]/option[{0}]'.format(yei)).click()
                # import ipdb; ipdb.set_trace()

            _url = browser.find_element_by_xpath('//div[@class="mh_comicpic"]/img')
            img_url = _url.get_attribute('src')

            # 保存图片到指定路径  
            if img_url != None:
                m += 1
                #保存图片数据  
                data = urllib.request.urlopen(img_url).read()
                f = open('{0}/{1}/{2}.jpg'.format(name, van, m), 'wb')
                f.write(data)
                f.close()
        xia = browser.find_element_by_xpath('//div[@class="mh_headpager"]/a[3]').get_attribute('href')
        # import ipdb; ipdb.set_trace()
        yield scrapy.Request(url=xia, callback=self.parse)
