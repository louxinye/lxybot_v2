# lxybot_v2
基于酷Q写的一个新版bot, 用于osu!新人群。老版本已经废弃不再更新  
使用前需要先进行httpapi和pysdk的配置(感谢作者)  
httpapi: https://github.com/richardchien/coolq-http-api (其中config配置文件我给出来了,在根目录下)  
pysdk: https://github.com/richardchien/cqhttp-python-sdk  

个人配置(仅供参考, 系统及版本差异并不清楚):  
操作系统: Window 10, 64位  
运行环境: Python 3.5.4  
IDE: PyCharm Community Edition 2017.2.3  

一些说明:  
main.py 主进程  
center 包括消息判断线程、定时任务线程  
function 用于实现各个具体在线功能  
offline 用于实现非在线功能, 比如利用爬虫和api录入大量osu玩家信息到数据库  
test 没啥用的玩意  
代码目前可放在 D:\Python POJ\lxybot_v2 里面  
