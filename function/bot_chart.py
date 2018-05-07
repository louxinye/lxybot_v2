# -*- coding: utf-8 -*-
# osu!新人群chart系统
from function import bot_osu
from function import bot_SQL


chart_bid = ['1580728']
now_turns = 1
force_mod = ['SO']
allow_mod = ['EZ', 'HR', 'HD', 'SD', 'PF', 'DT', 'NC', 'FL', 'SO']

def getChart():
	txt = '''本期chart内容如下:
bid: %s
强制Mod: %s
可选Mod: %s
允许fail: 否
得分方式: (acc^2 * combo^0.5 - userpp // 200 - miss) * v2mod_multiply * 1.6(if EZ)
!submit指令用于提交最近10次pass成绩,如果有包含本歌曲则进行得分计算''' % \
	      (chart_bid, getAllowMod(force_mod), getAllowMod(allow_mod))
	return txt

def getAllowMod(list_m):
	msg = ''
	for mod_name in list_m:
		if not msg:
			msg = msg + mod_name
		else:
			msg = msg + ',%s' % mod_name
	if not msg:
		msg = '无'
	return msg

def submitChart(user_qq):
	(msg, uid, pp) = bot_osu.searchUserInfo(user_qq)
	if not uid:
		return msg
	new_result = bot_osu.getUserRecent(uid, 0, max_num=20)
	if not new_result:
		msg = '游戏记录查询出错,请稍后再试'
		return msg
	(a1, current_chart) = myChart(user_qq)
	msg = '您未更新chart得分'
	for recent in new_result:
		if recent['beatmap_id'] not in chart_bid:  # 不是chart图，跳过
			continue
		if recent['rank'] == 'F':  # fail，跳过
			continue
		(mul, mod_list) = bot_osu.getMultiply(recent['enabled_mods'], EZbuff=1, Mtype=2)
		if not calAllowMod(mod_list):  # mod要求不符合，跳过
			continue
		bid = recent['beatmap_id']
		current_chart_score = getOldResult(current_chart, bid)
		new_chart_score = calChartScore(recent, pp, mul)
		# 对于每一条chart信息,0:uid,1:bid,2:turns,3:pp,4:c300,5:c100,6:c50,7:c0,8:score,9:combo,10:acc,11:rank,12:mod,13:mul,14:time,15:mode,16:result
		if new_chart_score > current_chart_score:
			acc = bot_osu.getAcc(recent['count300'], recent['count100'], recent['count50'], recent['countmiss'])
			if current_chart_score == 0:
				sql = 'INSERT INTO chart VALUES (%d, %s, %d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %.3f, %s, 0, %.2f)' % \
				    (uid, recent['beatmap_id'], now_turns, int(float(pp)), recent['count300'], recent['count100'], recent['count50'], recent['countmiss'],
	                recent['score'], recent['maxcombo'], acc, recent['rank'], recent['enabled_mods'], mul, recent['date'], new_chart_score)
			else:
				sql = 'UPDATE chart SET current_pp=%d, count300=%s, count100=%s, count50=%s, count0=%s, map_score=%s, map_combo=%s, map_acc=%s, ' \
				      'map_rank=%s, map_mod=%s, map_multiply=%.3f, map_time=%s, chart_score=%.2f WHERE uid=%s and bid=%s and turns=%s' %\
				      (int(float(pp)), recent['count300'], recent['count100'], recent['count50'], recent['countmiss'], recent['score'],
				       recent['maxcombo'], acc, recent['rank'], recent['enabled_mods'], mul, recent['date'], new_chart_score,
				       uid, bid, now_turns)
			bot_SQL.action(sql)
			msg = '您刷新了chart得分'
	return msg


def calAllowMod(mod_list):
	for forcemods in force_mod:
		if forcemods not in mod_list:
			return False
	for mods in mod_list:
		if mods not in allow_mod and mods not in force_mod:
			return False
	return True


def calChartScore(playmsg, user_pp, mod_mul):
	acc = float(bot_osu.getAcc(playmsg['count300'], playmsg['count100'], playmsg['count50'], playmsg['countmiss'])) / 100
	combo = playmsg['maxcombo']
	miss = playmsg['countmiss']
	result = (acc**2 * combo**0.5 - user_pp // 200 - miss) * mod_mul
	return result


def getOldResult(current_chart, bid):
	for oldplay in current_chart:
		if oldplay['turns'] == now_turns and oldplay['bid'] == bid:
			return oldplay['result']
	return 0


# 查询指定qq号的本期已有chart信息
def myChart(user_qq):
	chart_info = []
	sql = 'SELECT * FROM user where qq = \'%s\'' % user_qq
	result = bot_SQL.select(sql)
	if not result:
		msg = '您未绑定'
		return msg, chart_info
	uid = result[0][1]
	name = result[0][2]
	sql = 'SELECT * FROM chart WHERE uid = %s AND turns = %s' % (uid, now_turns)
	result = bot_SQL.select(sql)
	if not result:
		msg = '您没有相应chart成绩'
		return msg, chart_info
	# 对于每一条chart信息,0:uid,1:bid,2:turns,3:pp,4:c300,5:c100,6:c50,7:c0,8:score,9:combo,10:acc,11:rank,12:mod,13:mul,14:time,15:mode,16:result
	msg = '%s的成绩如下(第%d期)' % (name, now_turns)
	for chart in result:
		msg = msg + '\nbid: %s\nscore: %s\ncombo: %s\nacc: %s%%\n评分: %s\nchart得分: %s' % \
		            (chart[1], chart[8], chart[9], chart[10], chart[11], chart[16])
		chart_info.append({'turns': now_turns, 'bid': chart[1], 'result': chart[16]})
	return msg, chart_info
