import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors') # 忽略SSL错误
options.add_argument('disable-infobars')
options.add_argument("--disable-plugins-discovery")
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
options.add_argument('user-agent="{0}"'.format(user_agent))

proxy_info = {
    'host': '127.0.0.1',
    'port': 8080
}
# 使用代理
options.add_argument('--proxy-server={host}:{port}'.format(**proxy_info))

driver_path = os.path.join(os.getcwd(), r'chromedriver.exe')

browser = webdriver.Chrome(
    executable_path=driver_path,
    chrome_options=options
)
# 网页云音乐歌曲页面
url = 'https://music.163.com/#/song?id=408814900'
# 打开页面
browser.get(url)
# 等待页面加载
time.sleep(5)
# 切换到iframe里
browser.switch_to_frame('g_iframe')
# 找到iframe里面的播放按钮
a_play = browser.find_element_by_css_selector('#content-operation a[data-res-action="play"]')
# 触发播放（此时，就可以在中间人代码里查看ajax请求返回的数据了）
a_play.click()
