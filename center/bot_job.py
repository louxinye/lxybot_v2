# -*- coding: utf-8 -*-
import time
import datetime
from function import bot_IOfile
from function import bot_osu
from center import bot_global
from center import bot_msg
from function import bot_superstar


# bp监视任务,每执行一轮休息8分钟
def bpCareCenter(bot, maxcount):
    count = 0
    newstart = True
    while count < maxcount:
        time.sleep(30)
        print('定时bp监视任务触发')
        if bot_global.bp_watch:
            count = count + 1
            msg = '开始查询BP\n本次为bot启动后第%s次查询' % count
            print(msg)
            bot_global.user_bp_list_lock.acquire()  # 列表上锁
            for num in range(len(bot_global.user_bp_list)):
                user = bot_global.user_bp_list[num]
                user_id = user[20]["user_id"]
                score_mode = user[20]["user_mode"]
                group_list = user[20]["user_group"]
                new_bp = bot_osu.getUserBp(user_id, score_mode, max_num=20)
                if new_bp:
                    for i in range(0, 20):
                        if new_bp[i] != user[i]:
                            msg = '某人bp%s有变化,但是细节查询失败,将等待至下次查询' % (i+1)
                            (a1, user_name, a3, a4, a5, a6) = bot_osu.getUserInfo(user_id, score_mode, type_mode='id')
                            mode_name = bot_osu.getMode(score_mode)
                            if float(user[i]["pp"]) > float(new_bp[i]["pp"]):
                                map_id = user[i]["beatmap_id"]
                                map_info = bot_osu.getMapInfo(map_id, score_mode)
                                score_mod = bot_osu.getMod(user[i]["enabled_mods"])
                                old_pp = float(user[i]["pp"])
                                new_pp = float(bot_osu.getMapPlay(user_id, map_id, score_mode))
                                if user_name and map_info and new_pp:
                                    msg = '%s倒刷了一张图 (%s)\n谱面bid: %s\n%s\nMod: %s\n倒刷前的pp: %.2f\n现在的pp: %.2f'\
                                        % (user_name, mode_name, map_id, map_info, score_mod, old_pp, new_pp)
                                    update_bp = new_bp[0:20]
                                    update_bp.append({"user_id": user_id, "user_name": user_name, "user_mode": score_mode, "user_group": group_list})
                                    bot_global.user_bp_list[num] = update_bp
                                    bot_IOfile.write_pkl_data(bot_global.user_bp_list, 'data/data_bp_care_list.pkl')
                            else:
                                map_id = new_bp[i]["beatmap_id"]
                                map_info = bot_osu.getMapInfo(map_id, score_mode)
                                score_rank = bot_osu.getRank(new_bp[i]["rank"])
                                score_acc = bot_osu.getAcc(new_bp[i]["count300"], new_bp[i]["count100"], new_bp[i]["count50"], new_bp[i]["countmiss"])
                                score_mod = bot_osu.getMod(new_bp[i]["enabled_mods"])
                                score_pp = float(new_bp[i]["pp"])
                                if user_name and map_info:
                                    msg = '%s更新了bp%s (%s)\n谱面bid: %s\n%s\n评分: %s\nAcc: %s%%\nMod: %s\npp: %.2f'\
                                        % (user_name, i+1, mode_name, map_id, map_info, score_rank, score_acc, score_mod, score_pp)
                                    update_bp = new_bp[0:20]
                                    update_bp.append({"user_id": user_id, "user_name": user_name, "user_mode": score_mode, "user_group": group_list})
                                    bot_global.user_bp_list[num] = update_bp
                                    bot_IOfile.write_pkl_data(bot_global.user_bp_list, 'data/data_bp_care_list.pkl')
                            if not newstart:
                                for group in group_list:
                                    try:
                                        bot.send_group_msg(group_id=group, message=msg)
                                    except BaseException:
                                        print('群发消息出错, 群号: %s' % group)
                                break
            bot_global.user_bp_list_lock.release() # 列表解锁
            print('本轮查询结束')
            time.sleep(450)
            newstart = False
        else:
            time.sleep(30)
            newstart = True


# 定时踢人任务
def killCenter(bot):
    while(True):
        time.sleep(30)
        print('定时踢人倒计时触发')
        member_num = len(bot_global.kill_list)
        if member_num > 0:
            for i in range(member_num-1, -1, -1):
                bot_global.kill_list[i]['time'] = bot_global.kill_list[i]['time'] - 1
                if bot_global.kill_list[i]['time'] == 0:
                    group = bot_global.kill_list[i]['group']
                    qq = bot_global.kill_list[i]['qq']
                    msg = '操作执行成功: 踢出QQ号%s' % qq
                    del bot_global.kill_list[i]
                    try:
                        bot.set_group_kick(group_id=group, user_id=qq)
                        bot.send_group_msg(group_id=group, message=msg)
                    except:
                        pass
        time.sleep(30)


# pp超限踢人任务,每执行一轮休息1小时
def checkOutCenter(bot):
    while (True):
        time.sleep(100)
        print('定时pp超限踢人触发')
        now_day = datetime.date.today()
        for user in bot_global.user_check_out_list:
            context_temp = {'message_type': 'group', 'group_id': user['group'], 'user_id': user['qq'], 'message': '0'}
            if now_day >= user['deadline'] and bot_superstar.ignoreUserCheck(bot, context_temp) <= 1:
                msg = '!kill[CQ:at,qq=%s] ' % user['qq']
                context = {'message_type': 'group', 'group_id': user['group'], 'user_id': bot_global.host_list, 'message': msg, 'lxybot_sudo': True}
                bot.send_group_msg(group_id=user['group'], message=msg)
                bot_msg.MsgCenter(bot, context)
        time.sleep(3500)


# pp超限检测记录清除任务,每执行一轮休息12小时
def cleanCenter(bot):
    while(True):
        time.sleep(100)
        print('定时清除记录触发')
        bot_global.user_check_out_list.clear()
        time.sleep(43100)