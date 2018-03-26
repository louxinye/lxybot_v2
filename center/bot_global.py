# -*- coding: utf-8 -*-
# 多线程全局变量设置(目前仅有bp监视有这个需求)
import threading
from function import bot_IOfile


# BP监视开关
bp_watch = 0
# 恢复bp监视列表
user_bp_list = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_bp_care_list.pkl')
# 变量锁
user_bp_list_lock = threading.Lock()