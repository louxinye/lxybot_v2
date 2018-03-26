# -*- coding: utf-8 -*-
import random
import time
from center import bot_global
from function import bot_getmsg
from function import bot_suggest
from function import bot_health
from function import bot_noise
from function import bot_msgcheck
from function import bot_card
from function import bot_miegame
from function import bot_IOfile
from function import bot_osu


# 适用群列表: 主群，分群，喵呜，要饭，队群，贫民窟
group_list = [614892339, 514661057, 326389728, 641236878, 693657455, 204124585]
# 权限者qq号
dog_list = [3059841053]
# 当前复读次数, 若大于等于100则表示没有开启复读惩罚，和适用群一一对应
repeat_num = [100, 100, 100, 100, 100, 100]
# 当前复读语句, 和适用群一一对应
repeat_list = ['message_test', 'message_test', 'message_test', 'message_test', 'message_test', 'message_test']
# 咩羊游戏初始值
game_content = [[1, 1], [1, 1]]
# 正在使用咩羊游戏的玩家qq号
game_member = 0
# 咩羊游戏难度
game_diff = 0
# 恢复活动列表和健康列表
user_card_list = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_card_game_list.pkl')
health_list = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_health_list.pkl')


def MsgCenter(bot, context):
	global game_member
	global game_diff
	global bp_watch
	global game_content
	content = context['message']
	content = content.replace('&#91;', '[')
	content = content.replace('&#93;', ']')
	content = content.replace('&#44;', ',')
	content = content.replace('&amp;', '&')
	if content == '!hello':
		msg = 'v2.0: 响应测试成功'
		bot.send_group_msg(group_id=context['group_id'], message=msg)
	elif content == '!help':
		msg = bot_getmsg.getHelp()
		bot.send_group_msg(group_id=context['group_id'], message=msg)
	elif content == '!group':
		msg = bot_getmsg.suitL(group_list)
		bot.send_group_msg(group_id=context['group_id'], message=msg)

	# 适用群的群聊消息
	elif context['message_type'] == 'group' and context['group_id'] in group_list and context['user_id'] != 1061566571:
		group_i = group_list.index(context['group_id'])
		# 都有的功能
		if content == '!月常活动':
			msg = bot_getmsg.dalouCardGame()
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!找图系统':
			msg = bot_getmsg.ppSuggestSystem()
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif 'baka' in content:
			msg = 'ba—ka!!'
			bot.send_group_msg(group_id=context['group_id'], message=msg)

		# 月常活动
		elif '!start_card' in content:
			msg = atPeople(context['user_id']) + bot_card.startCard(context['user_id'], user_card_list, content)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!mygame':
			msg = atPeople(context['user_id']) + bot_card.userGameInfo(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!mycard':
			msg = atPeople(context['user_id']) + bot_card.userCardInfo(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!mymedal':
			msg = atPeople(context['user_id']) + bot_card.userMedalDetail(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!myMR':
			msg = atPeople(context['user_id']) + '请私聊查询'
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!myUR':
			msg = atPeople(context['user_id']) + '请私聊查询'
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!mySR':
			msg = atPeople(context['user_id']) + '请私聊查询'
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!myR':
			msg = atPeople(context['user_id']) + '请私聊查询'
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!myN':
			msg = atPeople(context['user_id']) + '请私聊查询'
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!update':
			msg = atPeople(context['user_id']) + bot_card.oneUserUpdate(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!pick':
			msg = atPeople(context['user_id']) + bot_card.pick1(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!pick11':
			msg = atPeople(context['user_id']) + bot_card.pick11(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!pickall':
			msg = atPeople(context['user_id']) + bot_card.pickall(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!fly':
			msg = atPeople(context['user_id']) + bot_card.fly1(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!pt_top':
			msg = bot_card.rankAll(user_card_list, 'pt_down')
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!pt_last':
			msg = bot_card.rankAll(user_card_list, 'pt_up')
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!mn_top':
			msg = bot_card.rankAll(user_card_list, 'mn_down')
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!mn_last':
			msg = bot_card.rankAll(user_card_list, 'mn_up')
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!lucky_top':
			msg = bot_card.rankAll(user_card_list, 'lucky_down')
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!lucky_last':
			msg = bot_card.rankAll(user_card_list, 'lucky_up')
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!card_p':
			msg = bot_card.gailv()
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!card_v':
			msg = bot_card.jiazhi()
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif content == '!rankme':
			msg = atPeople(context['user_id']) + bot_card.userRank(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif '!rank' in content:
			msg = bot_card.otherRank(user_card_list, content)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif '!card' in content:
			msg = bot_card.otherCardInfo(user_card_list, content)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif '!addmoney' in content:
			msg = bot_card.addMoney(context['user_id'], user_card_list)
			bot.send_group_msg(group_id=context['group_id'], message=msg)

		# 找图系统
		elif '!getmap' in content:
			bot.send_group_msg(group_id=context['group_id'], message='Dalou去找图了，请稍等')
			msg = atPeople(context['user_id']) + bot_suggest.searchMap(context['user_id'], content)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif '!banmap' in content:
			msg = atPeople(context['user_id']) + bot_suggest.banMap(context['user_id'], content)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif '!mapinfo' in content:
			msg = bot_suggest.infoMap(content)
			bot.send_group_msg(group_id=context['group_id'], message=msg)
		elif '!myid' in content:
			msg = atPeople(context['user_id']) + bot_osu.setid_sql(context['user_id'], content)
			bot.send_group_msg(group_id=context['group_id'], message=msg)

		# 去除新人群主群的其余指令
		elif group_i != 0:
			if content == '!健康系统':
				msg = bot_getmsg.healthSystem()
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!复读系统':
				msg = bot_getmsg.noiseSystem()
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!监视系统':
				msg = bot_getmsg.watchSystem()
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!咩羊游戏':
				msg = bot_getmsg.mieGame()
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!care':
				msg = bot_getmsg.careL(health_list)
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!dog':
				msg = bot_getmsg.dogL(dog_list)
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!bp':
				msg = bot_getmsg.bpL(bot_global.user_bp_list)
				bot.send_group_msg(group_id=context['group_id'], message=msg)

			# 发烟指令
			elif content == '!cnm':
				bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=5)
				msg = atPeople(context['user_id']) + '操作执行成功: 5秒'
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!rest':
				bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=3600)
				msg = atPeople(context['user_id']) + '操作执行成功: 1小时'
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!sleep':
				bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=21600)
				msg = atPeople(context['user_id']) + '操作执行成功: 6小时'
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif '!afk' in content:
				(smoke, msg1, msg2) = bot_msgcheck.afk(context['group_id'], context['user_id'], content)
				if msg1:
					msg = atPeople(context['user_id']) + msg1
				else:
					bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=smoke)
					msg = atPeople(context['user_id']) + '操作执行成功: %s' % msg2
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!sorry':
				smoke_minutes = random.randint(1, 60)
				bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=smoke_minutes*60)
				msg = atPeople(context['user_id']) + '操作执行成功: %s分' % smoke_minutes
				bot.send_group_msg(group_id=context['group_id'], message=msg)

			# 其余指令
			elif '!roll' in content:
				msg = atPeople(context['user_id']) + bot_msgcheck.roll(content)
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!health':
				msg = atPeople(context['user_id']) + bot_health.add(health_list, context['user_id'])
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!stop_h':
				msg = atPeople(context['user_id']) + bot_health.sub(health_list, context['user_id'])
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif '!set_bp' in content:
				bot_global.user_bp_list_lock.acquire()
				msg = atPeople(context['user_id']) + bot_osu.set_id(bot_global.user_bp_list, content)
				bot_global.user_bp_list_lock.release()
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif '!reset_bp' in content:
				bot_global.user_bp_list_lock.acquire()
				msg = atPeople(context['user_id']) + bot_osu.stop_set_id(bot_global.user_bp_list, content)
				bot_global.user_bp_list_lock.release()
				bot.send_group_msg(group_id=context['group_id'], message=msg)

			# 咩羊游戏
			elif '!game_mie' in content:
				(game_content, game_member, msg, diff) = bot_miegame.startGame(game_content, game_member, context['user_id'], content)
				if diff > 0:
					game_diff = diff
				msg = atPeople(context['user_id']) + msg
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif content == '!stop_g':
				if context['user_id'] == game_member:
					game_diff = 0
					game_member = 0
					msg = atPeople(context['user_id']) + '解除成功,游戏结束'
				else:
					msg = atPeople(context['user_id']) + '您并没有绑定该游戏'
				bot.send_group_msg(group_id=context['group_id'], message=msg)
			elif context['user_id'] == game_member:
				(msg1, msg2, gg) = bot_miegame.one_plus_one_check(game_content, content, game_diff)
				bot.send_group_msg(group_id=context['group_id'], message=msg1)
				if msg2:
					bot.send_group_msg(group_id=context['group_id'], message=msg2)
					if gg == 1:
						game_diff = 0
						game_member = ''
						msg = atPeople(context['user_id']) + '解除成功,游戏结束'
						bot.send_group_msg(group_id=context['group_id'], message=msg)

			# 狗管理指令集
			if context['user_id'] in dog_list:
				if content == '!watch':
					bot_global.bp_watch = 1
					msg = 'BP监视开启'
					bot.send_group_msg(group_id=context['group_id'], message=msg)
				elif content == '!stop_w':
					bot_global.bp_watch = 0
					msg = 'BP监视关闭'
					bot.send_group_msg(group_id=context['group_id'], message=msg)
				elif content == '!noise':
					msg = '复读惩罚启动'
					repeat_num[group_i] = 0
					bot.send_group_msg(group_id=context['group_id'], message=msg)
				elif content == '!stop_n':
					msg = '复读惩罚关闭'
					repeat_num[group_i] = 100
					bot.send_group_msg(group_id=context['group_id'], message=msg)
				elif '!ban_card' in content:
					msg = bot_card.stopCard(user_card_list, content)
					bot.send_group_msg(group_id=context['group_id'], message=msg)
				elif content == '!updateall':
					bot.send_group_msg(group_id=context['group_id'], message='开始全体更新打图记录')
					msg = bot_card.allUserUpdate(user_card_list)
					bot.send_group_msg(group_id=context['group_id'], message=msg)
					bot.send_group_msg(group_id=context['group_id'], message='更新完毕')
				elif content == '!myrct':
					msg = '!recent'
					bot.send_group_msg(group_id=context['group_id'], message=msg)

			# 健康监督触发
			if context['user_id'] in health_list:
				t_hour = int(time.strftime('%H', time.localtime(time.time())))
				t_minute = int(time.strftime('%M', time.localtime(time.time())))
				if 0 <= t_hour <= 7:
					smoke = 6 * 60 * 60 - t_hour * 60 * 60 - t_minute * 60
					bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=smoke)
					msg = atPeople(context['user_id']) + '现在是半夜,请睡觉了'
					if context['user_id'] == game_member:
						game_diff = 0
						game_member = 0
						msg = msg + '\n您的咩羊游戏被强制解除'
					bot.send_group_msg(group_id=context['group_id'], message=msg)

			# 复读检测触发
			if repeat_num[group_i] < 100:
				t = bot_noise.check(group_i, repeat_list, repeat_num, content)
				if t == 1:
					bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=300)
					msg = atPeople(context['user_id']) + '求求你别复读了'
					bot.send_group_msg(group_id=context['group_id'], message=msg)
				if t == 2:
					bot.send_group_msg(group_id=context['group_id'], message=content)

	# 私聊指令
	elif context['message_type'] == 'private' and context['user_id'] != 1061566571:
		print('有个傻逼私聊你了: %s' % content)
		if content == '!月常活动':
			msg = bot_getmsg.dalouCardGame()
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!找图系统':
			msg = bot_getmsg.ppSuggestSystem()
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!start_card' in content:
			msg = '注册指令只支持下列群号内使用:'
			for group in group_list:
				msg = msg + '\n%s' % group
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!mygame':
			msg = bot_card.userGameInfo(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!mycard':
			msg = bot_card.userCardInfo(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!mymedal':
			msg = bot_card.userMedalDetail(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!myMR':
			msg = bot_card.userCardDetail(context['user_id'], user_card_list, 0)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!myUR':
			msg = bot_card.userCardDetail(context['user_id'], user_card_list, 1)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!mySR':
			msg = bot_card.userCardDetail(context['user_id'], user_card_list, 2)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!myR':
			msg = bot_card.userCardDetail(context['user_id'], user_card_list, 3)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!myN':
			msg = bot_card.userCardDetail(context['user_id'], user_card_list, 4)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!update':
			msg = bot_card.oneUserUpdate(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!pick':
			msg = bot_card.pick1(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!pick11':
			msg = bot_card.pick11(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!pickall':
			msg = bot_card.pickall(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!fly':
			msg = bot_card.fly1(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!pt_top':
			msg = bot_card.rankAll(user_card_list, 11, maxnum=15)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!pt_last':
			msg = bot_card.rankAll(user_card_list, 12, maxnum=15)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!mn_top':
			msg = bot_card.rankAll(user_card_list, 21, maxnum=15)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!mn_last':
			msg = bot_card.rankAll(user_card_list, 22, maxnum=15)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!lucky_top':
			msg = bot_card.rankAll(user_card_list, 31, maxnum=15)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!lucky_last':
			msg = bot_card.rankAll(user_card_list, 32, maxnum=15)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!card_p':
			msg = bot_card.gailv()
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!card_v':
			msg = bot_card.jiazhi()
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif content == '!rankme':
			msg = bot_card.userRank(context['user_id'], user_card_list)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!rank' in content:
			msg = bot_card.otherRank(user_card_list, content)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!card' in content:
			msg = bot_card.otherCardInfo(user_card_list, content)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!getmap' in content:
			bot.send_private_msg(user_id=context['user_id'], message='Dalou去找图了，请稍等')
			msg = bot_suggest.searchMap(context['user_id'], content, suggest_num=15)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!banmap' in content:
			msg = bot_suggest.banMap(context['user_id'], content)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!mapinfo' in content:
			msg = bot_suggest.infoMap(content)
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!myid' in content:
			msg = '绑定指令只支持下列群号内使用:'
			for group in group_list:
				msg = msg + '\n%s' % group
			bot.send_private_msg(user_id=context['user_id'], message=msg)
		elif '!remove' in content:
			(msg, num) = bot_msgcheck.remove(content)
			if num > -1:
				bot.set_group_ban(group_id=group_list[num], user_id=context['user_id'], duration=0)
			bot.send_private_msg(user_id=context['user_id'], message=msg)


# 加上艾特人的CQ头
def atPeople(user_qq):
	return '[CQ:at,qq=%s] \n' % user_qq
