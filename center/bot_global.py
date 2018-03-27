# -*- coding: utf-8 -*-
# 多线程全局变量设置(目前仅有bp监视有这个需求)
import threading
from function import bot_IOfile


# BP监视开关
bp_watch = 0
# 恢复bp监视列表
user_bp_list = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_bp_care_list.pkl')
# 变量锁,对内容有改动的指令需要加锁以实现互斥(对只读指令则采取鸵鸟策略)
user_bp_list_lock = threading.Lock()
user_card_list_lock = threading.Lock()
health_list_lock = threading.Lock()
noise_list_lock = threading.Lock()
game_mie_lock = threading.Lock()
sql_action_lock = threading.Lock()
