# -*- coding: utf-8 -*-
# 开发中........
from urllib import parse,request
import requests
import json

headers = {
    'Accept' : '*/*',
    'Accept-Language' : 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests' : '1',
    'content-type': 'text/plain;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
}

textmod={0:"好啊",1:"就算你是一流工程师",2:"就算你出报告再完美",3:"我叫你改报告你就要改",4:"毕竟我是客户",5:"客户了不起啊",6:"sorry 客户真的了不起",7:"以后叫他天天改报告",8:"111111"}
text = {"0": "111", "1": "222", "2": "333", "3": "444", "4": "555", "5": "666", "6": "777", "7": "888", "8": "111111"}
# textmod = json.dumps(textmod).encode(encoding='utf-8')
# textmod = parse.urlencode(textmod).encode(encoding='utf-8')


url='https://sorry.xuty.tk/api/sorry/make'
req = requests.post(url=url,data=text,headers=headers)
print(req.text)
# res = req.json()
# print(res.decode(encoding='utf-8'))