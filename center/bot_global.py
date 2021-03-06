# -*- coding: utf-8 -*-
# 全局设置
import threading
from function import bot_IOfile


# BP监视开关
bp_watch = 1
# 恢复bp监视列表,用户当日是否被检查列表,用户将被超限踢出列表
user_bp_list = bot_IOfile.read_pkl_data('data/data_bp_care_list.pkl')
user_check_in_list = bot_IOfile.read_pkl_data('data/data_check_in_list.pkl')
user_check_out_list = bot_IOfile.read_pkl_data('data/data_check_out_list.pkl')
# 变量锁,对内容有改动的指令需要加锁以实现互斥(对只读指令则采取鸵鸟策略)
user_bp_list_lock = threading.Lock()
user_card_list_lock = threading.Lock()
health_list_lock = threading.Lock()
noise_list_lock = threading.Lock()
game_mie_lock = threading.Lock()
sql_action_lock = threading.Lock()
super_star_lock = threading.Lock()
check_out_lock = threading.Lock()


def getGroupList(list_g):
	for i in range(len(list_g)):
		if list_g[i] < len(group_total_list):
			list_g[i] = group_total_list[list_g[i]]
	return list_g


# 适用群列表: 0主群,1分群,2后花园,3避难所,4粉丝群,5队群,6娱乐群,7贫民窟,8管理群,9测试群
group_total_list = [614892339, 758120648, 514661057, 885984366, 669361496, 693657455, 102171745, 204124585, 695600319, 939344921]
discuss_total_list = []
# 新人群代号:
group_main_list = getGroupList([0, 1, 2, 3])
# chart群代号:
group_chart_list = getGroupList([0, 3, 8])
# 新人群管理群代号:
group_main_admin_list = getGroupList([8])
# 管理员存在的群代号:
group_dog_list = getGroupList([0, 1, 2, 3, 4, 6, 8, 9])
# 权限者qq号
dog_list = [1061566571, 3059841053, 1208604740, 962549599, 178039743, 1094452372, 986176546, 447503971]
# 本bot的qq号
host_list = [3082577334]
# 屏蔽qq号,群聊时无视这些人的发言
ignore_list = [1677323371, 122866607, 1394932996, 1335734629, 2839098896, 1091569752, 2478057279, 3527783823]
# 白名单qq号,群聊时无视这些人的pp超限检测
white_list = [2680306741, 1149483077, 2636027237, 2429299722, 2643555740, 2307282906, 2639140005, 2308394636, 1559449817]
# 主群临时回家qq号
white_temp_list = [759609157, 97512825]
# 当前复读次数, 若大于等于100则表示没有开启复读惩罚,和适用群一一对应
repeat_num = [100, 100, 100, 0, 0, 0, 0, 100, 100, 0]
# 当前复读语句, 和适用群一一对应
repeat_list = ['message', 'message', 'message', 'message', 'message', 'message', 'message', 'message', 'message', 'message']
# 踢人列表
kill_list = []


