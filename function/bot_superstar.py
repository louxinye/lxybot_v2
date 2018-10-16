# -*- coding: utf-8 -*-
# 带有参数的部分指令检查系统
import random
import re
import datetime
from center import bot_global
from function import bot_osu

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

# 返回值:多少pp开始计算踢人时间，多少pp为极限上限，每提升多少pp则减少一天倒计时
def maxPPCheck(group):
	if group not in bot_global.group_main_list:
		return 99999, 99999, 99999
	num = bot_global.group_main_list.index(group)
	if num == 0:
		return 2000, 2500, 3
	elif num == 1:
		return 4400, 4500, 1
	else:
		return 99999, 99999, 1

def nowPPCheck(qq):
	result = bot_osu.searchUserInfo(qq, update=False)
	if not result['uid']:
		return -1, -1, -1
	else:
		return result['pp'], result['uid'], result['name']


def checkout(group, qq, uid, name, days):
	now_day = datetime.date.today()
	kill_day = now_day + datetime.timedelta(days=days)
	success = False
	msg = '本条语句为debug专用,请无视'
	for user_will_be_kill in bot_global.user_check_out_list:
		if user_will_be_kill['qq'] == qq:
			success = True
			user_will_be_kill['uid'] = uid
			user_will_be_kill['name'] = name
			msg = '每日提醒: 您将在指定日期后离开本群: %s' % kill_day
			if kill_day < user_will_be_kill['deadline']:
				user_will_be_kill['deadline'] = kill_day
				msg = '由于您的出色进阶水平,将提前至下列日期离开本群: %s' % kill_day
			break
	if not success:
		bot_global.user_check_out_list.append({'group': group, 'qq': qq, 'uid': uid, 'name': name, 'deadline': kill_day})
		msg = '您已达到进阶水平,将在指定日期后离开本群: %s' % kill_day
	return msg