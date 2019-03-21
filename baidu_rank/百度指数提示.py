import os
import json
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
# *************** 专业造假 ###################

browser.get('http://index.baidu.com/v2/rank/index.html#/industryrank/star')

'''
len(browser.find_elements_by_css_selector('.date-item'))
len(browser.find_elements_by_css_selector('.date-icon-up'))
browser.find_element_by_css_selector('.date-icon-up').click()
browser.find_element_by_css_selector('.date-item')
browser.find_element_by_css_selector('.date-item:nth-of-type(3)')
browser.find_elements_by_css_selector('.date-item:nth-of-type(3)')[0].text
browser.find_elements_by_css_selector('.date-item:nth-of-type(2)')[0].click()
'''
