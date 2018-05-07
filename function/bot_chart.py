# -*- coding: utf-8 -*-
# osu!新人群chart系统
from function import bot_osu
from function import bot_SQL


chart_bid = [1580728, 155929]
now_turns = 1
force_mod = []
allow_mod = ['EZ', 'HR', 'HD', 'SD', 'PF', 'DT', 'NC', 'FL', 'SO']

def getChart():
    txt = '''本期chart内容如下:
bid: %s
强制Mod: %s
可选Mod: %s
允许fail: 否
得分方式: 太长了懒得写
!submit指令用于提交最近15次成绩,如果有包含本歌曲则进行得分计算''' % \
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
    new_result = bot_osu.getUserRecent(uid, 0, max_num=15)
    if not new_result:
        msg = '游戏记录查询出错,请稍后再试'
        return msg
    (a1, current_chart) = myChart(user_qq)
    msg = ''
    old_result_list = getOldResult(current_chart)
    update_list = []
    for recent in new_result:
        bid = int(recent['beatmap_id'])
        if bid not in chart_bid:  # 不是chart图，跳过
            continue
        if recent['rank'] == 'F':  # fail，跳过
            continue
        (mul, mod_list) = bot_osu.getMultiply(recent['enabled_mods'], EZbuff=1.6, Mtype=2)
        if not calAllowMod(mod_list):  # mod要求不符合，跳过
            continue
        index = chart_bid.index(bid)
        new_chart_score = calChartScore(recent, pp, mul)
        print('uid:%s, bid:%s, old:%.2f, new:%.2f' % (uid, bid, old_result_list[index], new_chart_score))
        if new_chart_score > old_result_list[index] + 0.005:
            for i in range(len(update_list)):
                if update_list[i]['beatmap_id'] == bid:
                    del update_list[i]
                    break
            update_list.append(recent)
            old_result_list[index] = new_chart_score
    if not update_list:
        msg = '您未更新chart成绩'
        return msg
    msg = '您更新了下列chart成绩:'
    for update in update_list:
    # 对于每一条chart信息,0:uid,1:bid,2:turns,3:pp,4:c300,5:c100,6:c50,7:c0,8:score,9:combo,10:acc,11:rank,12:mod,13:mul,14:time,15:mode,16:result
        bid = int(update['beatmap_id'])
        acc = bot_osu.getAcc(update['count300'], update['count100'], update['count50'], update['countmiss'])
        new_chart_score = old_result_list[chart_bid.index(bid)]
        sql = 'SELECT * FROM chart WHERE uid=%s and bid=%s and turns=%s' % (uid, update['beatmap_id'], now_turns)
        aaa = bot_SQL.select(sql)
        if aaa:
            sql = 'UPDATE chart SET current_pp=%s, count300=%s, count100=%s, count50=%s, count0=%s, map_score=%s, map_combo=%s, map_acc=%s, ' \
                  'map_rank=\'%s\', map_mod=%s, map_multiply=%.3f, map_time=\'%s\', chart_score=%.2f WHERE uid=%s and bid=%s and turns=%s' % \
                  (int(float(pp)), update['count300'], update['count100'], update['count50'], update['countmiss'], update['score'],
                   update['maxcombo'], acc, update['rank'], update['enabled_mods'], mul, update['date'], new_chart_score,
                   uid, bid, now_turns)
            msg = msg + '\n\nbid: %s\n得分: %.2f → %.2f' % (bid, aaa[0][16], new_chart_score)
        else:
            sql = 'INSERT INTO chart VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \'%s\', %s, %.3f, \'%s\', \'0\', %.2f)' % \
                  (uid, bid, now_turns, int(float(pp)), update['count300'], update['count100'], update['count50'], update['countmiss'],
                   update['score'], update['maxcombo'], acc, update['rank'], update['enabled_mods'], mul, update['date'], new_chart_score)
            msg = msg + '\n\nbid: %s\n得分: 0 → %.2f' % (bid, new_chart_score)
        bot_SQL.action(sql)
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
    combo = int(playmsg['maxcombo'])
    pp = int(float(user_pp))
    miss = int(playmsg['countmiss'])
    result = (15 + acc**2 * combo**0.5 - pp * 0.004 - miss * 0.2) * mod_mul
    return result


def getOldResult(current_chart):
    result = [0, 0]
    for i in range(len(chart_bid)):
        for oldplay in current_chart:
            if oldplay['turns'] == now_turns and oldplay['bid'] == chart_bid[i]:
                result[i] = oldplay['result']
                break
    return result


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
        msg = msg + '\n\nbid: %s\n评分: %s\nchart得分: %.2f\n时间: %s' % \
                    (chart[1], chart[11], chart[16], chart[14])
        chart_info.append({'turns': now_turns, 'bid': chart[1], 'result': chart[16]})
    return msg, chart_info
