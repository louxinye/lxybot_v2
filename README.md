# lxybot_v2
基于酷Q写的一个新版bot, 用于osu!新人群。老版本已经废弃不再更新  
使用前需要先进行httpapi和pysdk的配置(感谢作者)  
httpapi: https://github.com/richardchien/coolq-http-api (其中config配置文件我给出来了,在根目录下)  
pysdk: https://github.com/richardchien/cqhttp-python-sdk  

个人配置(仅供参考, 系统及版本差异并不清楚):  
操作系统: Windows 10, 64位  
运行环境: Python 3.5.4  
数据库: MySQL Workbench 6.3 CE  
IDE: PyCharm Community Edition 2017.2.3  

一些说明:  
main.py 主进程  
center 包括消息判断线程、定时任务线程等并存放部分全局变量  
function 用于实现各个具体在线功能  
offline 用于实现非在线功能, 比如利用爬虫和api录入大量osu玩家信息到数据库  
data 存储pkl文件, 为了防止一些问题我先不提供数据, 目前里面存的都是空列表  
plugin 计算pp的插件，被我魔改了一些……  
test 没啥用的玩意  
