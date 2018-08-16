# -*- coding: utf-8 -*-
# 带有参数的部分指令检查系统
import random
import re
from center import bot_global

def maxDiffCheck(group):
	if group not in bot_global.group_main_list:
		return 99999
	num = bot_global.group_main_list.index(group)
	if num == 0:
		return 540
	elif num == 1:
		return 650
	else:
		return 99999

def nowDiffCheck(content):
	check_at = re.findall(r'\[CQ:at,qq=([1-9][0-9]*)\]', content)
	check_stars = re.findall(r'stars: ([1-9][0-9]*.[0-9]*)\* \|', content)
	if check_at and check_stars:
		user_qq = int(check_at[0])
		map_diff = int(float(check_stars[0]) * 100)
		return map_diff, user_qq
	else:
		return 0, 0