# -*- coding: utf-8 -*-
# 全局设置
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

# 适用群列表: 0主群,1分群,2喵呜,3要饭,4队群,5娱乐群,6贫民窟
group_total_list = [614892339, 514661057, 326389728, 641236878, 693657455, 102171745, 204124585]
discuss_total_list = []
# 新人群列表:
group_main_list = [614892339, 514661057]
# bp监视适用群列表:
group_bp_list = [514661057, 326389728, 693657455, 102171745]
# 管理员存在的群:
group_dog_list = [614892339, 514661057, 326389728, 102171745]
# 权限者qq号
dog_list = [1061566571, 3059841053]
# 本bot的qq号
host_list = [3082577334]
# 屏蔽qq号,群聊时无视这些人的发言
ignore_list = [1677323371, 122866607, 1394932996, 1335734629, 2839098896, 1091569752, 2478057279]
# 当前复读次数, 若大于等于100则表示没有开启复读惩罚,和适用群一一对应
repeat_num = [0, 0, 0, 0, 0, 0, 0]
# 当前复读语句, 和适用群一一对应
repeat_list = ['message', 'message', 'message', 'message', 'message', 'message', 'message']

