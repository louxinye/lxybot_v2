# -*- coding: utf-8 -*-
# osu!新人群chart系统
import re
from function import bot_osu
from function import bot_SQL


chart_bid = [1113308, 1116219, 476149]
now_turns = 1
force_mod = []
allow_mod = ['EZ', 'HR', 'HD', 'SD', 'PF', 'DT', 'NC', 'FL', 'SO']


# 提交chart,效果如下:更新用户信息
def submitChart(user_qq):
    userinfo = bot_osu.searchUserInfo(user_qq, update=False)
    uid = userinfo['uid']
    name = userinfo['name']
    pp = int(float(userinfo['pp']))
    if not uid:
        return userinfo['msg']
    new_result = bot_osu.getUserRecent(uid, 0, max_num=15)
    if not new_result:
        msg = '游戏记录查询出错,请稍后再试'
        return msg
    current_chart = myChart(user_qq)['chart_info']
    old_result_list = getOldResult(current_chart)
    update_list = []
    for recent in new_result:
        bid = int(recent['beatmap_id'])
        if bid not in chart_bid:  # 不是chart图，跳过
            continue
        if recent['rank'] == 'F':  # fail，跳过
            continue
        (mul, mod_list) = bot_osu.getMultiply(recent['enabled_mods'], EZbuff=1.8, Mtype=2)
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
        old_chart_info = bot_SQL.select(sql)
        if old_chart_info:
            sql = 'UPDATE chart SET current_pp=%s, count300=%s, count100=%s, count50=%s, count0=%s, map_score=%s, map_combo=%s,' \
                  'map_acc=%s, map_rank=\'%s\', map_mod=%s, map_multiply=%.3f, map_time=\'%s\', chart_score=%.2f, user_name=\'%s\'' \
                  'WHERE uid=%s and bid=%s and turns=%s' % (pp, update['count300'], update['count100'], update['count50'],
                   update['countmiss'], update['score'], update['maxcombo'], acc, update['rank'], update['enabled_mods'],
                   mul, update['date'], new_chart_score, name, uid, bid, now_turns)
            msg = msg + '\n\nbid: %s\n得分: %.2f → %.2f' % (bid, old_chart_info[0][16], new_chart_score)
        else:
            sql = 'INSERT INTO chart VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \'%s\', %s, %.3f, \'%s\', \'0\', %.2f, \'%s\')'\
                  % (uid, bid, now_turns, pp, update['count300'], update['count100'], update['count50'], update['countmiss'],update['score'],
                     update['maxcombo'], acc, update['rank'], update['enabled_mods'], mul, update['date'], new_chart_score, name)
            msg = msg + '\n\nbid: %s\n得分: 0 → %.2f' % (bid, new_chart_score)
        bot_SQL.action(sql)
    return msg


# 判断玩家开启的mod是否符合要求
def calAllowMod(mod_list):
    for forcemods in force_mod:
        if forcemods not in mod_list:
            return False
    for mods in mod_list:
        if mods not in allow_mod and mods not in force_mod:
            return False
    return True


# chart得分计算
def calChartScore(playmsg, user_pp, mod_mul):
    acc = float(bot_osu.getAcc(playmsg['count300'], playmsg['count100'], playmsg['count50'], playmsg['countmiss'])) / 100
    combo = int(playmsg['maxcombo'])
    pp = int(float(user_pp))
    miss = int(playmsg['countmiss'])
    result = (15 + acc**2 * combo**0.5 - pp * 0.004 - miss * 0.25) * mod_mul
    return result


# 获取对应bid编号的旧chart成绩,如果无成绩则输出0
def getOldResult(current_chart):
    result = [0, 0, 0]
    for i in range(len(chart_bid)):
        for oldplay in current_chart:
            if oldplay['turns'] == now_turns and oldplay['bid'] == chart_bid[i]:
                result[i] = oldplay['result']
                break
    return result


# 查询指定qq号的本期已有chart信息,返回字典的列表,如果指定getMsg为True则会详细输出文本信息
def myChart(user_qq, getMsg=False):
    chart_info = []
    sql = 'SELECT * FROM user where qq = \'%s\'' % user_qq
    result = bot_SQL.select(sql)
    if not result:
        msg = '您未绑定'
        return {'msg': msg, 'chart_info':chart_info}
    uid = result[0][1]
    name = result[0][2]
    sql = 'SELECT * FROM chart WHERE uid = %s AND turns = %s' % (uid, now_turns)
    result = bot_SQL.select(sql)
    if not result:
        msg = '您没有相应chart成绩'
        return {'msg': msg, 'chart_info': chart_info}
    # 对于每一条chart信息,0:uid,1:bid,2:turns,3:pp,4:c300,5:c100,6:c50,7:c0,8:score,9:combo,10:acc,11:rank,12:mod,13:mul,14:time,15:mode,16:result
    msg = '%s的成绩如下(第%d期)' % (name, now_turns)
    for chart in result:
        if getMsg:
            rankmsg = getRankInfo(chart[2], chart[1])
            rank = 0
            for i in range(len(rankmsg)):
                if rankmsg[i][0] == uid:
                    rank = i + 1
            msg = msg + '\n\nbid: %s\n评分: %s\nchart得分: %.2f\n排名: %s/%s\n时间: %s' % \
                        (chart[1], chart[11], chart[16], rank, len(rankmsg), chart[14])
        chart_info.append({'turns': chart[2], 'bid': chart[1], 'result': chart[16]})
    return {'msg': msg, 'chart_info':chart_info}


# 获取指定chart图的全体信息,且默认按照总分降顺排序
def getRankInfo(turns, bid):
    sql = 'SELECT uid, user_name, chart_score FROM chart WHERE bid = %s and turns = %s ORDER BY chart_score DESC' % (bid, turns)
    result = bot_SQL.select(sql)
    return result


# 获取指定chart图的前几名的文本信息,若不指定bid则默认输出全体chart图
def outputRankMsg(turns, bid=0, single_max_num=7, all_max_num=3):
    if bid:
        result = getRankInfo(turns, bid)
        msg = 'bid: %s' % bid
        for i in range(min(single_max_num, len(result))):
           msg = msg + '\n%s: %s (%s)' % (i+1, result[i][1], result[i][2])
    else:
        msg = '第%s期全部chart排名一览' % turns
        for bid in chart_bid:
            msg = msg + '\n\nbid: %s' % bid
            result = getRankInfo(turns, bid)
            for i in range(min(all_max_num, len(result))):
                msg = msg + '\n%s: %s (%s)' % (i+1, result[i][1], result[i][2])
    return msg


# 获取chart图排名信息,接受用户指令且用于最终输出
def rankChart(content):
    if content == '!chart_top':
        msg = outputRankMsg(now_turns)
    elif '!chart_top ' in content:
        check_bid = re.match(r'^!chart_top ([1-9][0-9]*)$', content)
        if check_bid:
            bid = int(check_bid.group(1))
            if bid not in chart_bid:
                msg = 'bid: %s\n不是本期chart指定图' % bid
            else:
                msg = outputRankMsg(now_turns, bid=bid)
        else:
            msg = '您的!chart_top指令使用错误'
    else:
        msg = '无法识别,推测您是想使用指令!chart_top x(x为参数)'
    return msg


def getChart():
    txt = '''本期chart内容如下:
bid: %s
强制Mod: %s
可选Mod: %s
允许fail: 否
得分方式: 太长了懒得写
!submit指令用于提交最近15次成绩,如果有包含本歌曲则进行得分计算''' \
          % (printAllow(chart_bid), printAllow(force_mod), printAllow(allow_mod))
    return txt


def printAllow(list_m):
    msg = ''
    for name in list_m:
        if not msg:
            msg = msg + '%s' % name
        else:
            msg = msg + ',%s' % name
    if not msg:
        msg = '无'
    return msg