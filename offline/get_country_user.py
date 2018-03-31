# -*- coding: utf-8 -*-
# 获取某个国家的osu前1w名的用户uid
import re
from urllib import request
from function import bot_IOfile


headers = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language' : 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
}
# user_list = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot\data\data_user_ru_list.pkl')
user_list = []
for pages in range(1,201):
    url = 'https://osu.ppy.sh/p/pp/?c=CN&m=0&s=3&o=1&f=0&page=%s' % pages
    req = request.Request(url, headers=headers)
    page = request.urlopen(req).read()
    html = page.decode("utf-8")
    if len(html) < 300:
        print('某页错误')
        continue
    check_id = re.findall(r'<a.*? href=\'/u/[0-9]*\'>', html)
    check_pp = re.findall(r'<span style=\'font-weight:bold\'>(.*?)pp</span>', html)
    for i in range(50):
        if 'color:gray' in check_id[i]:
            print('%s.%s跳过' % (pages, i))
        else:
            get_uid = re.findall(r'/u/([0-9]*)', check_id[i])
            uid = int(get_uid[0])
            pp = int(check_pp[i].replace(',', '', 1))
            print('%s.%s成功, %s, %s' % (pages, i, uid, pp))
            user_list.append({'uid': uid, 'pp': pp})
    if pages%10 == 0:
        bot_IOfile.write_pkl_data(user_list, 'D:\Python POJ\lxybot_v2\data\data_user_cn_list.pkl')
        print('保存!')
