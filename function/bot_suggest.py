# -*- coding: utf-8 -*-
import re
from function import bot_SQL
from function import bot_osu


min_member = 1  # 一首歌至少有几个人打过，才进入后续推荐指数计算


def infoMap(content):
    if content == '!mapinfo':
        return '倒是告诉我要查哪个图啊'
    check_map = re.match(r'^!mapinfo ([1-9][0-9]*)$', content)
    if check_map:
        bid = int(check_map.group(1))
        map_info = bot_osu.get_map(bid, '0', getlength=1)
        if not map_info:
            map_info =  '网络爆炸了,查询地图失败'
        sql = 'SELECT * FROM bp_mode0_msg WHERE `bid` = %s ORDER BY `mod` DESC' % bid
        result = bot_SQL.select(sql)
        if not result:
            msg = '\n数据库中没有其余详细信息'
        else:
            msg = '\n数据库中有如下信息:'
            total_list = list(result)
            i_now = 0
            i_max = len(total_list)
            # 数据库返回的每一条信息中,0:uid,1:bp_rank,2:bid,3:mod,4:score_pp,5:user_pp.6:mod_new,7:pp_new
            user_last = total_list[0][5]
            user_top = total_list[0][5]
            pp_last = total_list[0][4]
            pp_top = total_list[0][4]
            user_total = total_list[0][5]
            pp_total = total_list[0][4]
            user_num = 1
            while True:
                i_now = i_now + 1
                if i_now != i_max and total_list[i_now][3] == total_list[i_now-1][3]:
                    if user_last > total_list[i_now][5]:
                        user_last = total_list[i_now][5]
                    if user_top < total_list[i_now][5]:
                        user_top = total_list[i_now][5]
                    if pp_last > total_list[i_now][4]:
                        pp_last = total_list[i_now][4]
                    if pp_top < total_list[i_now][4]:
                        pp_top = total_list[i_now][4]
                    user_total = user_total + total_list[i_now][5]
                    user_num = user_num + 1
                    pp_total = pp_total + total_list[i_now][4]
                else:
                    msg = msg + '\n【%s】共%s条记录' % (bot_osu.get_mod(total_list[i_now-1][3]), user_num)
                    msg = msg + '\n玩家%s-%s(平均%s)' % (user_last, user_top, int(user_total/user_num))
                    msg = msg + '\n成绩%s-%s(平均%s)' % (pp_last, pp_top, int(pp_total/user_num))
                    if i_now == i_max:
                        break
                    user_last = total_list[i_now][5]
                    user_top = total_list[i_now][5]
                    pp_last = total_list[i_now][4]
                    pp_top = total_list[i_now][4]
                    user_total = total_list[i_now][5]
                    pp_total = total_list[i_now][4]
                    user_num = 1
        return map_info + msg


def banMap(user_qq, content):
    if content == '!banmap':
        return '倒是告诉我要屏蔽哪个图啊'
    check_map = re.match(r'^!banmap ([1-9][0-9]*)$', content)
    if check_map:
        bid = int(check_map.group(1))
        sql = 'SELECT * FROM user WHERE qq = %s AND mode = 0' % user_qq
        result = bot_SQL.select(sql)
        if not result:
            msg = '您未绑定'
            return msg
        uid = result[0][1]
        sql = 'SELECT * FROM bp_ban WHERE uid = %d AND bid = %d AND mode = 0' % (uid, bid)
        result = bot_SQL.select(sql)
        if result:
            msg = '您早就屏蔽此图了!'
            return msg
        sql = 'INSERT INTO bp_ban VALUES (%d, %d, 0, %s)' % (uid, bid, user_qq)
        success = bot_SQL.action(sql)
        if success:
            msg = '屏蔽成功!'
        else:
            msg = '数据库出错,请联系Dalou'
        return msg
    else:
        return '您的!banmap指令使用错误'


def searchMap(user_qq, content, suggest_num=5):
    check_msg1 = re.match(r'^!getmap with (.*) for (.*)$', content)
    check_msg2 = re.match(r'^!getmap for (.*)$', content)
    check_msg3 = re.match(r'^!getmap with (.*)$', content)
    check_msg4 = re.match(r'^!getmap$', content)
    if check_msg1:
        (input_mod, input_user) = allCal(content)
        if input_mod < 0:
            return '您输入的Mod有误!'
        (uid, name, pp, pc, tth, acc) = bot_osu.get_info(input_user, '0')
    elif check_msg2:
        input_mod = -999
        input_user = nameCal(content)
        (uid, name, pp, pc, tth, acc) = bot_osu.get_info(input_user, '0')
    elif check_msg3 or check_msg4:
        if check_msg3:
            input_mod = modCal(content)
            if input_mod < 0:
                return '您输入的Mod有误!'
        else:
            input_mod = -999
        sql = 'SELECT * FROM user WHERE qq = %s AND mode = 0' % user_qq
        result = bot_SQL.select(sql)
        if not result:
            msg = '您未绑定'
            return msg
        uid = result[0][1]
        (uid, name, pp, pc, tth, acc) = bot_osu.get_info(uid, '0', type_mode='id')
        if uid:
            sql = 'UPDATE user SET name = \'%s\', pp = %d, pc = %d, tth = %d, acc= %.2f WHERE qq = %d and mode = 0' % (name, pp, pc, tth, acc, user_qq)
            bot_SQL.action(sql)
    else:
        return '您的!getmap指令使用错误'
    if not uid:
        return '用户查询出错,请稍后再试'
    if pp > 6000 or pp < 800:
        return '本推荐只支持pp在800-6000的玩家'
    bp_result = bot_osu.get_bp(uid, '0')
    if not bp_result:
        return 'bp查询出错,请稍后再试'
    bp_bid = []
    for bp in bp_result:
        bp_bid.append(int(bp['beatmap_id']))
    pp_min = pp - 150
    pp_max = pp + 350
    if input_mod == -999:
        sql = 'SELECT * FROM bp_mode0_msg WHERE `user_pp` > %d AND `user_pp` < %d ' \
              'AND bid NOT IN (SELECT bid FROM bp_ban WHERE uid = %s AND mode = 0) ORDER BY bid DESC' % \
              (pp_min, pp_max, uid)
    else:
        sql = 'SELECT * FROM bp_mode0_msg WHERE `user_pp` > %d AND `user_pp` < %d AND `mod_new` = %d ' \
              'AND bid NOT IN (SELECT bid FROM bp_ban WHERE uid = %s AND mode = 0) ORDER BY bid DESC' % \
              (pp_min, pp_max, input_mod, uid)
    result = bot_SQL.select(sql)
    total_list = list(result)
    suggest_list = []
    i_max = len(total_list)
    i_now = 0
    # 数据库返回的每一条信息中,0:uid,1:bp_rank,2:bid,3:mod,4:score_pp,5:user_pp.6:mod_new,7:pp_new
    while True:
        if i_now > i_max - min_member:  # 查询到头的时候，结束
            break
        if total_list[i_now][2] in bp_bid:  # 如果这张图已经打过了，跳过
            i_now = i_now + 1
            continue
        if total_list[i_now][2] != total_list[i_now + min_member - 1][2]:  # 如果这张图打的人少于n个，跳过
            i_now = i_now + 1
            continue
        for j in range(i_now + min_member - 1, i_max):  # 至少有n个人打了一张你没打过的图，开始计算
            if j == i_max - 1 or total_list[i_now][2] != total_list[j + 1][2]:
                e_pp = 0  # 期望pp
                e_good = 0  # 推荐指数
                for songs in range(i_now, j + 1):
                    e_pp = e_pp + total_list[songs][7]
                    e_good = e_good + 50 - total_list[songs][1]
                e_pp = int(e_pp / (j - i_now + 1))
                e_good = int(e_good / 100)
                suggest_list.append(
                    {'bid': total_list[i_now][2], 'mod': total_list[i_now][6], 'pp': e_pp, 'good': e_good})
                i_now = j  # 处理完毕后，索引直接跳转到相同歌曲的最后那一位
                break
        i_now = i_now + 1
    suggest_list.sort(key=lambda x: x['good'], reverse=True)
    if not suggest_list:
        msg = '你太强了, bot不知道该给你推荐什么图才合适'
    else:
        msg = '%s的推荐图如下:\nBid, Mod, pp, 推荐指数' % name
    for i in range(min(suggest_num, len(suggest_list))):
        mod_name = bot_osu.get_mod(suggest_list[i]['mod'])
        msg = msg + '\n%s, %s, %s, %s' % (
        suggest_list[i]['bid'], mod_name, suggest_list[i]['pp'], suggest_list[i]['good'])
    return msg


def modCal(content):
    if content == '!getmap with none' or content == '!getmap with None' or content == '!getmap with NONE':
        return 0
    check_mod = re.match(r'^!getmap with (\w*)$', content)
    if check_mod:
        mod_name = check_mod.group(1)
        mod_id = modIdCal(mod_name)
        return mod_id
    else:
        return -1


def nameCal(content):
    check_name = re.match(r'^!getmap for (.*)$', content)
    if check_name:
        user_name = check_name.group(1)
        return user_name
    else:
        return -1


def allCal(content):
    check_all = re.match(r'^!getmap with (\w*) for (.*)$', content)
    if check_all:
        mod_name = check_all.group(1)
        user_name = check_all.group(2)
        mod_id = modIdCal(mod_name)
        return mod_id, user_name
    else:
        return -1, -1


# 输入mod名字,屏蔽其中部分mod，并输出modid
def modIdCal(mod_name):
    if mod_name == 'None' or mod_name == 'none' or mod_name == 'NONE':
        return 0
    if not mod_name:
        return -1
    if len(mod_name)%2 != 0:
        return -1
    num = int(len(mod_name)/2)
    mod_id = 0
    mod_pick = [0,0,0,0,0,0]
    for i in range(num):
        get = mod_name[2*i: 2*i+2]
        if get == 'hd' or get == 'HD':
            if mod_pick[0] == 0:
                mod_pick[0] = 1
            else:
                return -1
        elif get == 'nf' or get == 'NF' or get == 'sd' or get == 'SD' or get == 'pf' or get == 'PF':
            if mod_pick[1] == 0:
                mod_pick[1] = 1
            else:
                return -1
        elif get == 'so' or get == 'SO':
            if mod_pick[2] == 0:
                mod_pick[2] = 1
            else:
                return -1
        elif get == 'nc' or get == 'NC'or get == 'dt' or get == 'DT':
            if mod_pick[3] == 0:
                mod_pick[3] = 1
            else:
                return -1
            mod_id = mod_id + 64
        elif get == 'ht' or get == 'HT':
            if mod_pick[3] == 0:
                mod_pick[3] = 1
            else:
                return -1
            mod_id = mod_id + 256
        elif get == 'hr' or get == 'HR':
            if mod_pick[4] == 0:
                mod_pick[4] = 1
            else:
                return -1
            mod_id = mod_id + 16
        elif get == 'ez' or get == 'EZ':
            if mod_pick[4] == 0:
                mod_pick[4] = 1
            else:
                return -1
            mod_id = mod_id + 2
        elif get == 'fl' or get == 'FL':
            if mod_pick[5] == 0:
                mod_pick[5] = 1
            else:
                return -1
            mod_id = mod_id + 1024
        else:
            return -1
    return mod_id
