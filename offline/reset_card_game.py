# -*- coding: utf-8 -*-
# 初始化玩家数据,一般用于月初更新
from function import bot_IOfile

list_card = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_card_game_list.pkl')
for i in range(len(list_card)):
	list_card[i]['medal'] = [0, 0, 0, 0, 0, 0, 0]
	list_card[i]['card'] = [[], [], [], [], []]
	list_card[i]['money'] = 100
	list_card[i]['total_money'] = 100
	list_card[i]['pt'] = 0
	list_card[i]['fly'] = 0
	list_card[i]['lucky'] = 0
	list_card[i]['lucky_rate'] = 0
	list_card[i]['boom_money'] = 0
	list_card[i]['boom_cost'] = 30
	list_card[i]['bonus_pt'] = 0
bot_IOfile.write_pkl_data(list_card, 'D:\Python POJ\lxybot_v2\data\data_card_game_list.pkl')