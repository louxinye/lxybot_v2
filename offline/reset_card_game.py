# -*- coding: utf-8 -*-
# 初始化玩家数据,一般用于月初更新
from function import bot_IOfile

list_card = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_card_game_list.pkl')
newlist = []
for i in range(len(list_card)-1,-1,-1):
	if list_card[i]['pt_total'] < 1 and list_card[i]['money_total'] < 1000:
		del list_card[i]
	else:
		card_member = list_card[i]['qq']
		osu_id = list_card[i]['uid']
		name = list_card[i]['name']
		pc = list_card[i]['pc']
		tth = list_card[i]['tth']
		medal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		user_info = {'qq': card_member, 'uid': osu_id, 'name': name, 'pc': pc, 'tth': tth, 'medal': medal,
		             'card': [[], [], [], [], []], 'money_now': 100, 'money_total': 100, 'money_boom_total': 0,
		             'money_boom_cost': 30, 'money_smoke': 0, 'money_bonus': 0, 'pt_total': 0, 'pt_bonus': 0,
		             'lucky': 0, 'lucky_rate': 0, 'fly': 0, 'num_pick': 0, 'num_fly': 0}
		newlist.append(user_info)
bot_IOfile.write_pkl_data(newlist, 'D:\Python POJ\lxybot_v2\data\data_card_game_list.pkl')