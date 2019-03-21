# -*- coding: utf-8 -*-
import scrapy
import os
import json
import time

from baidu_rank.items import BaiduRankItem
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('disable-infobars')
options.add_argument("--disable-plugins-discovery")
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
options.add_argument('user-agent="{0}"'.format(user_agent))

driver_path = os.path.join(os.getcwd(), r'chromedriver.exe')

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
webdriver.Chrome.add_script = add_script # 这里（webdriver.Chrome）可能需要改，当调用不同的驱动时
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
pprint(existed)
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

class BdSpider(scrapy.Spider):
    name = 'bd'
    allowed_domains = ['index.baidu.com']
    start_urls = ['http://index.baidu.com/v2/rank/index.html#/industryrank/star']
    # browser = webdriver.Chrome(r'F:\爬虫\5、网络爬虫框架\baidu_rank\chromedriver.exe')
    browser.get(start_urls[0])
    
    def parse(self, response):
        _click = browser.find_elements_by_css_selector('.date-item')
        for i in _click:
            _click = browser.find_element_by_css_selector('.date-text-con')
            _click.click() 
            # time.sleep(1)
            i.click()
            item = BaiduRankItem()
            item['zhou'] = browser.find_element_by_xpath('//span[@class="date-text-con"]/span[1]/text()')
            # item['zhou'] = response.xpath('//span[@class="date-text-con"]/span[1]/text()').extract()
            item['_id'] = response.xpath('//div[@class="left"]/span[1]/text()').extract()
            item['name'] = response.xpath('//div[@class="left"]/span[2]/text()').extract()
            item['index'] = response.xpath('//div[@class="right"]/div[2]/span[1]/text()').extract()
            yield item
