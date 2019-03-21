'''
mitmdump -s mitm-scripy-01.py
'''
import ipdb
import json
import requests
from pprint import pprint
from mitmproxy import ctx


def request(flow):
    """
    修改请求数据 
    """
    if flow.request.url.endswith('/'):
        # ipdb.set_trace()
        pass
    pass

def response(flow):
    """
    修改应答数据 
    """
    # if flow.request.url.endswith('/'):
    if 'music.163.com/weapi/song/enhance/player/url' in flow.request.url:
        # ipdb.set_trace()
        pprint(json.loads(flow.response.text))
        print(flow.request.cookies)
        print('=' * 50)
        print(flow.request.headers)
        print('=' * 50)
        # 将响应内容改为百度的页面响应
        # baidu_resp_text = requests.get('https://www.baidu.com/').text
        # flow.response.text = baidu_resp_text
    pass
