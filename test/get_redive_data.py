# -*- coding: utf-8 -*-
# osu相关系统
import requests
import json
import re
import math
from function import bot_IOfile
from function import bot_SQL
from center import bot_global
from plugin import console_calc


headers = {
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-Language' : 'zh-CN,zh;q=0.9',
    'cache-Control': 'max-age=0',
    'upgrade-Insecure-Requests' : '1',
    'referer':'https://pcrdwiki.xyz/zh-hans/unit/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
}


# 输入用户名或uid(此时需要指明type_mode为id)，输出确切的用户信息
def getCardInfo(card_id):
    url = 'https://pcrdwiki.xyz/zh-hans/unit_data/%s' % card_id
    res = getUrl(url)
    if not res:
        return {}
    result = json.loads(res.text)
    if not result:
        return {}
    else:
        return result


# request请求
def getUrl(url):
    try:
        res = requests.get(url=url, headers=headers, params=None, timeout=3)
        return res
    except requests.exceptions.RequestException:
        return 0


rst = getCardInfo(100901)
if len(rst):
    print(len(rst["equipment_enhance"]))
    for a in rst["equipment_enhance"]:
        print(a)
else:
    print('network error')