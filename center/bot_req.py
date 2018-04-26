# -*- coding: utf-8 -*-
import re
from center import bot_global


def ReqCenter(bot, context):
	# 新人群加群验证
	if context['request_type'] == 'group' and context['group_id'] in bot_global.group_main_list and context[
		'sub_type'] == 'add':
		user_group = context['group_id']
		group_type = getGroupName(bot_global.group_main_list.index(user_group))
		user_qq = context['user_id']
		check_msg = re.findall(r'\n答案：(.*)', context['message'])
		if check_msg:
			user_msg = check_msg[0]
		else:
			user_msg = context['message']
		msg = '收到新人群加群申请\n群号: %s\n群类型: %s\n申请者: %s\n验证信息: %s' % (user_group, group_type, user_qq, user_msg)
		for group in bot_global.group_main_admin_list:
			bot.send_group_msg(group_id=group, message=msg)


def getGroupName(i):
	if i == 0:
		return '主群'
	if i == 1:
		return '分群'
	return '鬼知道什么群'