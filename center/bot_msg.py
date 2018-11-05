# -*- coding: utf-8 -*-
import random
import time
import re
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
from function import bot_chart
from function import bot_superstar


# 咩羊游戏初始值
game_content = [[1, 1], [1, 1]]
# 正在使用咩羊游戏的玩家qq号
game_member = 0
# 咩羊游戏难度
game_diff = 0
# 恢复活动列表和健康列表
user_card_list = bot_IOfile.read_pkl_data('data/data_card_game_list.pkl')
health_list = bot_IOfile.read_pkl_data('data/data_health_list.pkl')
egg_list = bot_IOfile.read_pkl_data('data/data_egg_list.pkl')


def MsgCenter(bot, context):
    global game_member
    global game_diff
    global game_content

    # 转义字符与指令字符处理
    content = context['message']
    content = content.replace('&#91;', '[')
    content = content.replace('&#93;', ']')
    content = content.replace('&#44;', ',')
    content = content.replace('&amp;', '&')
    if content and content[0] == '！':
        content = content.replace('！', '!', 1)
    print(content)

    # 无权限指令
    if content == '!hello':
        msg = '响应测试成功'
        reply(bot, context, msg, atPeople=False)
    elif content == '!help':
        msg = bot_getmsg.getHelp()
        reply(bot, context, msg, atPeople=False)
    elif content == '!group':
        msg = bot_getmsg.suitL(bot_global.group_total_list)
        reply(bot, context, msg, atPeople=False)

    # 权限判断
    if context['user_id'] in bot_global.host_list and 'lxybot_sudo' not in context:
        pass
    elif context['message_type'] == 'group' and (context['group_id'] not in bot_global.group_total_list or context['user_id'] in bot_global.ignore_list):
        pass
    elif context['message_type'] == 'discuss' and context['discuss_id'] not in bot_global.discuss_total_list:
        pass
    else:
        if content == '!月常活动':
            msg = bot_getmsg.dalouCardGame()
            reply(bot, context, msg, atPeople=False)
        elif content == '!chart活动':
            msg = bot_getmsg.chartSystem()
            reply(bot, context, msg, atPeople=False)
        elif content == '!找图系统':
            msg = bot_getmsg.ppSuggestSystem()
            reply(bot, context, msg, atPeople=False)
        elif content == '!健康系统':
            msg = bot_getmsg.healthSystem()
            reply(bot, context, msg, atPeople=False)
        elif content == '!监视系统':
            msg = bot_getmsg.watchSystem()
            reply(bot, context, msg, atPeople=False)
        elif content == '!咩羊游戏':
            msg = bot_getmsg.mieGame()
            reply(bot, context, msg, atPeople=False)
        elif content == '!抽烟系统':
            msg = bot_getmsg.smokeSystem()
            reply(bot, context, msg, atPeople=False)
        elif content == '!欢送系统':
            msg = bot_getmsg.farewellSystem()
            reply(bot, context, msg, atPeople=False)
        elif content == '!dog':
            msg = bot_getmsg.dogL(bot_global.dog_list)
            reply(bot, context, msg, atPeople=False)
        elif content == '!egg':
            msg = bot_getmsg.eggL(egg_list)
            reply(bot, context, msg, atPeople=False)
        elif content == '!kill':
            msg = bot_getmsg.killL(bot_global.kill_list)
            reply(bot, context, msg, atPeople=False)
        elif content == '!farewell':
            msg = bot_getmsg.farewellL(bot_global.user_check_out_list, context['user_id'])
            reply(bot, context, msg, atPeople=False)
        elif content == '!whitelist':
            msg = bot_getmsg.whiteL(bot_global.white_list, bot_global.white_temp_list)
            reply(bot, context, msg, atPeople=False)
        elif '!roll' in content:
            msg = bot_msgcheck.roll(content)
            reply(bot, context, msg, atPeople=True)

        # osu基本功能
        elif '!myid' in content:
            bot_global.sql_action_lock.acquire()
            msg = bot_osu.setSQL(context['user_id'], content)
            bot_global.sql_action_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!mypp':
            bot_global.sql_action_lock.acquire()
            userinfo = bot_osu.searchUserInfo(context['user_id'])
            bot_global.sql_action_lock.release()
            reply(bot, context, userinfo['msg'], atPeople=True)
        elif content == '!myrct':
            # 此指令存在bug，为了避免死锁暂时先取消加锁
            # bot_global.sql_action_lock.acquire()
            msg = bot_osu.searchUserRecent(context['user_id'])
            # bot_global.sql_action_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!dalou':
            bot_global.sql_action_lock.acquire()
            msg = bot_osu.dalou(context['user_id'])
            bot_global.sql_action_lock.release()
            reply(bot, context, msg, atPeople=True)

        # 月常活动
        elif '!start_card' in content:
            if not verify(context, {'group': bot_global.group_main_list}):
                msg = '该指令不支持在此处使用'
            else:
                bot_global.user_card_list_lock.acquire()
                msg = bot_card.startCard(context['user_id'], user_card_list, content)
                bot_global.user_card_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!mygame':
            msg = bot_card.userGameInfo(context['user_id'], user_card_list)
            reply(bot, context, msg, atPeople=True)
        elif content == '!mycard':
            msg = bot_card.userCardInfo(context['user_id'], user_card_list)
            reply(bot, context, msg, atPeople=True)
        elif content == '!mymedal':
            msg = bot_card.userMedalDetail(context['user_id'], user_card_list)
            reply(bot, context, msg, atPeople=True)
        elif content == '!myMR':
            msg = bot_card.userCardDetail(context['user_id'], user_card_list, 0, contact=context['message_type'])
            reply(bot, context, msg, atPeople=True)
        elif content == '!myUR':
            msg = bot_card.userCardDetail(context['user_id'], user_card_list, 1, contact=context['message_type'])
            reply(bot, context, msg, atPeople=True)
        elif content == '!mySR':
            msg = bot_card.userCardDetail(context['user_id'], user_card_list, 2, contact=context['message_type'])
            reply(bot, context, msg, atPeople=True)
        elif content == '!myR':
            msg = bot_card.userCardDetail(context['user_id'], user_card_list, 3, contact=context['message_type'])
            reply(bot, context, msg, atPeople=True)
        elif content == '!myN':
            msg = bot_card.userCardDetail(context['user_id'], user_card_list, 4, contact=context['message_type'])
            reply(bot, context, msg, atPeople=True)
        elif content == '!update':
            bot_global.user_card_list_lock.acquire()
            msg = bot_card.oneUserUpdate(context['user_id'], user_card_list)
            bot_global.user_card_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!pick':
            bot_global.user_card_list_lock.acquire()
            msg = bot_card.pick1(context['user_id'], user_card_list)
            bot_global.user_card_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!pick11':
            bot_global.user_card_list_lock.acquire()
            msg = bot_card.pick11(context['user_id'], user_card_list)
            bot_global.user_card_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!pickall':
            bot_global.user_card_list_lock.acquire()
            msg = bot_card.pickall(context['user_id'], user_card_list)
            bot_global.user_card_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!fly':
            bot_global.user_card_list_lock.acquire()
            msg = bot_card.fly1(context['user_id'], user_card_list)
            bot_global.user_card_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!pt_top':
            msg = bot_card.rankAll(user_card_list, 'pt_down', contact=context['message_type'])
            reply(bot, context, msg, atPeople=False)
        elif content == '!pt_last':
            msg = bot_card.rankAll(user_card_list, 'pt_up', contact=context['message_type'])
            reply(bot, context, msg, atPeople=False)
        elif content == '!mn_top':
            msg = bot_card.rankAll(user_card_list, 'mn_down', contact=context['message_type'])
            reply(bot, context, msg, atPeople=False)
        elif content == '!mn_last':
            msg = bot_card.rankAll(user_card_list, 'mn_up', contact=context['message_type'])
            reply(bot, context, msg, atPeople=False)
        elif content == '!lucky_top':
            msg = bot_card.rankAll(user_card_list, 'lucky_down', contact=context['message_type'])
            reply(bot, context, msg, atPeople=False)
        elif content == '!lucky_last':
            msg = bot_card.rankAll(user_card_list, 'lucky_up', contact=context['message_type'])
            reply(bot, context, msg, atPeople=False)
        elif content == '!rankme':
            msg = bot_card.userRank(context['user_id'], user_card_list)
            reply(bot, context, msg, atPeople=True)
        elif '!addmoney' in content:
            bot_global.user_card_list_lock.acquire()
            # msg = bot_card.addMoney(context['user_id'], user_card_list)
            msg = '别想着作弊啦,努力打图去吧'
            bot_global.user_card_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif context['message_type'] == 'group' and context['group_id'] in bot_global.group_main_list and '!boom' in content:
            bot_global.user_card_list_lock.acquire()
            (msg, success, user, smoke1, smoke2) = bot_card.sendBoom(user_card_list, context['user_id'], content)
            bot_global.user_card_list_lock.release()
            if success:
                bot.set_group_ban(group_id=context['group_id'], user_id=user, duration=smoke1)
                bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=smoke2)
            reply(bot, context, msg, atPeople=True)

        # 找图系统
        elif '!getmap' in content:
            reply(bot, context, 'Dalou去找图了,请稍等', atPeople=False)
            bot_global.sql_action_lock.acquire()
            msg = bot_suggest.searchMap(context['user_id'], content, contact=context['message_type'])
            bot_global.sql_action_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif '!banmap' in content:
            bot_global.sql_action_lock.acquire()
            msg = bot_suggest.banMap(context['user_id'], content)
            bot_global.sql_action_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif '!mapinfo' in content:
            bot_global.sql_action_lock.acquire()
            msg = bot_suggest.infoMap(content, contact=context['message_type'])
            bot_global.sql_action_lock.release()
            reply(bot, context, msg, atPeople=False)

        # 监视系统
        elif '!set_bp' in content:
            if not verify(context, {'group': bot_global.group_total_list}):
                msg = '该指令不支持在此处使用'
            else:
                bot_global.user_bp_list_lock.acquire()
                msg = bot_osu.setCare(bot_global.user_bp_list, content, context['group_id'])
                bot_global.user_bp_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif '!reset_bp' in content:
            if not verify(context, {'group': bot_global.group_total_list}):
                msg = '该指令不支持在此处使用'
            else:
                bot_global.user_bp_list_lock.acquire()
                msg = bot_osu.stopCare(bot_global.user_bp_list, content, context['group_id'])
                bot_global.user_bp_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!bp':
            if not verify(context, {'group': bot_global.group_total_list}):
                msg = '该指令不支持在此处使用'
            else:
                msg = bot_getmsg.bpL(bot_global.user_bp_list, context['group_id'])
            reply(bot, context, msg, atPeople=False)

        # 健康系统
        elif content == '!health':
            bot_global.health_list_lock.acquire()
            msg = bot_health.add(health_list, context['user_id'])
            bot_global.health_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!stop_h':
            bot_global.health_list_lock.acquire()
            msg = bot_health.sub(health_list, context['user_id'])
            bot_global.health_list_lock.release()
            reply(bot, context, msg, atPeople=True)
        elif content == '!care':
            msg = bot_getmsg.careL(health_list)
            reply(bot, context, msg, atPeople=False)

        # 咩羊游戏
        elif '!game_mie' in content:
            (msg, diff) = bot_miegame.startGame(game_member, context['user_id'], content)
            if diff > 0:
                game_member = context['user_id']
                game_diff = diff
                game_content = [[1, 1], [1, 1]]
            reply(bot, context, msg, atPeople=True)
        elif content == '!stop_g':
            if context['user_id'] == game_member:
                game_member = 0
                msg = '解除成功,游戏结束'
            else:
                msg = '您并没有绑定该游戏'
            reply(bot, context, msg, atPeople=True)

        # 其余具体情况具体分析
        else:
            # 超级权限指令
            if context['user_id'] in bot_global.dog_list:
                if content == '!watch':
                    bot_global.bp_watch = 1
                    msg = 'BP监视开启'
                    reply(bot, context, msg, atPeople=False)
                elif content == '!stop_w':
                    bot_global.bp_watch = 0
                    msg = 'BP监视关闭'
                    reply(bot, context, msg, atPeople=False)
                elif '!ban_card' in content:
                    bot_global.user_card_list_lock.acquire()
                    msg = bot_card.stopCard(user_card_list, content)
                    bot_global.user_card_list_lock.release()
                    reply(bot, context, msg, atPeople=False)
                elif content == '!updateall':
                    reply(bot, context, '开始全体更新打图记录', atPeople=False)
                    bot_global.user_card_list_lock.acquire()
                    msg = bot_card.allUserUpdate(user_card_list)
                    bot_global.user_card_list_lock.release()
                    reply(bot, context, msg, atPeople=False)
                elif '!update' in content:
                    bot_global.user_card_list_lock.acquire()
                    msg = bot_card.certainUserUpdate(user_card_list, content)
                    bot_global.user_card_list_lock.release()
                    reply(bot, context, msg, atPeople=False)
                elif '!unbind' in content:
                    bot_global.sql_action_lock.acquire()
                    msg = bot_osu.unsetSQL(content)
                    bot_global.sql_action_lock.release()
                    reply(bot, context, msg, atPeople=False)
                elif '!stop_mie' in content:
                    game_member = 0
                    msg = '咩羊游戏解除'
                    reply(bot, context, msg, atPeople=False)
                elif '!测试' in content:
                    msg = '%s' % bot_msgcheck.getGroupMemberInfo(bot, context['group_id'], context['user_id'])
                    reply(bot, context, msg, atPeople=False)
                elif context['message_type'] == 'group' and context['group_id'] in bot_global.group_dog_list:
                    if '!smoke' in content:
                        (msg, success, user, smoke) = bot_msgcheck.sendSmoke(content)
                        if success:
                            bot.set_group_ban(group_id=context['group_id'], user_id=user, duration=smoke)
                        reply(bot, context, msg, atPeople=False)
                    elif '!unsmoke' in content:
                        (msg, success, user) = bot_msgcheck.removeSmoke(content)
                        if success:
                            bot.set_group_ban(group_id=context['group_id'], user_id=user, duration=0)
                        reply(bot, context, msg, atPeople=False)
                    elif '!kill' in content:
                        msg = bot_msgcheck.sendKill(bot, bot_global.kill_list, context['group_id'], content)
                        reply(bot, context, msg, atPeople=False)
                    elif '!stop_k' in content:
                        msg = bot_msgcheck.stopKill(bot_global.kill_list, context['group_id'], content)
                        reply(bot, context, msg, atPeople=False)


            # 需要管理员身份的群聊指令
            if context['message_type'] == 'group' and context['group_id'] in bot_global.group_dog_list:
                if content == '!cnm':
                    smoke = random.randint(5, 100)
                    bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=smoke)
                    msg = '操作执行成功: %s秒' % smoke
                    reply(bot, context, msg, atPeople=True)
                elif content == '!rest':
                    bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=3600)
                    msg = '操作执行成功: 1小时'
                    reply(bot, context, msg, atPeople=True)
                elif content == '!sleep':
                    bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=21600)
                    msg = '操作执行成功: 6小时'
                    reply(bot, context, msg, atPeople=True)
                elif '!afk' in content:
                    (smoke, msg1, msg2) = bot_msgcheck.afk(context['group_id'], context['user_id'], content)
                    if msg1:
                        msg = msg1
                    else:
                        bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=smoke)
                        msg = '操作执行成功: %s' % msg2
                    reply(bot, context, msg, atPeople=True)

            # 超星检测
            if context['message_type'] == 'group' and context['group_id'] in bot_global.group_main_list:
                if context['user_id'] == 2680306741:
                    max_diff = bot_superstar.maxDiffCheck(context['group_id'])
                    (now_diff, user_qq) = bot_superstar.nowDiffCheck(content)
                    if now_diff > max_diff:
                        smoke = min(2591940, (now_diff - max_diff) * 10 * 60)
                        msg = '核能侦测启动成功: %s秒' % smoke
                        bot.set_group_ban(group_id=context['group_id'], user_id=user_qq, duration=smoke)
                        reply(bot, context, msg, atPeople=False)

            # 主群chart活动
            if context['message_type'] == 'group' and context['group_id'] in bot_global.group_chart_list:
                if content == '!chart':
                    msg = bot_chart.getChart()
                    reply(bot, context, msg, atPeople=False)
                elif content == '!submit':
                    bot_global.sql_action_lock.acquire()
                    # msg = '本期chart已经结束'
                    msg = bot_chart.submitChart(context['user_id'])
                    bot_global.sql_action_lock.release()
                    reply(bot, context, msg, atPeople=True)
                elif content == '!mychart':
                    bot_global.sql_action_lock.acquire()
                    chartinfo = bot_chart.myChart(context['user_id'],getMsg=True)
                    bot_global.sql_action_lock.release()
                    reply(bot, context, chartinfo['msg'], atPeople=True)
                elif '!chart_top' in content:
                    bot_global.sql_action_lock.acquire()
                    msg = bot_chart.rankChart(content)
                    bot_global.sql_action_lock.release()
                    reply(bot, context, msg, atPeople=False)

            # 新人群彩蛋
            if context['message_type'] == 'group' and context['group_id'] in bot_global.group_main_list:
                for egg in egg_list:
                    if '[CQ:' not in content:
                        check_egg = re.match(r'%s' % egg['expression'], content)
                        if check_egg:
                            reply(bot, context, egg['reply'], atPeople=False)
                            bot_global.sql_action_lock.acquire()
                            if not egg['unlock_qq']:
                                egg['unlock_name'] = bot_osu.searchUserInfo(context['user_id'])['name']
                                egg['unlock_qq'] = context['user_id']
                                if egg['unlock_name'] and egg['unlock_name'] != '0':
                                    msg = '大伙注意啦, %s解锁了%s号彩蛋' % (egg['unlock_name'], egg['id'])
                                    msg1 = '全部彩蛋解锁完毕，恭喜%s得到撒泼特一个月' % egg['unlock_name']
                                else:
                                    msg = '大伙注意啦, QQ号%s解锁了%s号彩蛋' % (egg['unlock_qq'], egg['id'])
                                    msg1 = '全部彩蛋解锁完毕，恭喜QQ号%s得到撒泼特一个月' % egg['unlock_qq']
                                bot_IOfile.write_pkl_data(egg_list, 'data/data_egg_list.pkl')
                                reply(bot, context, msg, atPeople=False)
                                all_unlock = True
                                for eggs in egg_list:
                                    if not eggs['unlock_qq']:
                                        all_unlock = False
                                        break
                                if all_unlock:
                                    reply(bot, context, msg1, atPeople=False)
                            bot_global.sql_action_lock.release()
                            break

            # 健康系统计算
            if context['message_type'] == 'group' and context['user_id'] in health_list:
                t_hour = int(time.strftime('%H', time.localtime(time.time())))
                t_minute = int(time.strftime('%M', time.localtime(time.time())))
                if 0 <= t_hour <= 6:
                    smoke = 6 * 60 * 60 - t_hour * 60 * 60 - t_minute * 60
                    bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=smoke)
                    msg = '现在是半夜,请睡觉了'
                    if context['user_id'] == game_member:
                        game_member = 0
                        msg = msg + '\n您的咩羊游戏被强制解除'
                    reply(bot, context, msg, atPeople=True)

            # 咩羊游戏计算
            if context['user_id'] == game_member:
                bot_global.game_mie_lock.acquire()
                (msg1, msg2, gg) = bot_miegame.one_plus_one_check(game_content, content, game_diff)
                bot_global.game_mie_lock.release()
                reply(bot, context, msg1, atPeople=True)
                if msg2:
                    reply(bot, context, msg2, atPeople=True)
                    if gg == 1:
                        game_member = 0
                        msg = '解除成功,游戏结束'
                        reply(bot, context, msg, atPeople=False)

            # 复读触发
            if context['message_type'] == 'group' and context['group_id'] in bot_global.group_total_list:
                group_i = bot_global.group_total_list.index(context['group_id'])
                if '!' in content or '！' in content or '~' in content or '~' in content or '[CQ:' in content:
                    pass
                elif bot_global.repeat_num[group_i] >= 100:
                    pass
                else:
                    bot_global.noise_list_lock.acquire()
                    t = bot_noise.check(group_i, bot_global.repeat_list, bot_global.repeat_num, content)
                    bot_global.noise_list_lock.release()
                    if t == 2:
                        reply(bot, context, content, atPeople=False)

            # 私聊解禁
            if context['message_type'] == 'private' and '!remove' in content:
                '''
                if context['user_id'] in bot_global.dog_list:
                    (msg, remove_group_i) = bot_msgcheck.remove(content)
                    if remove_group_i > -1:
                        if bot_global.group_total_list[remove_group_i] not in bot_global.group_dog_list:
                            msg = '臣妾做不到啊(不是管理员)'
                        else:
                            bot.set_group_ban(group_id=bot_global.group_total_list[remove_group_i], user_id=context['user_id'], duration=0)
                else:
                '''
                msg = '此功能暂时关闭'
                reply(bot, context, msg, atPeople=False)

            # 群发公告
            if context['message_type'] == 'private' and '!send' in content:
                if context['user_id'] in bot_global.dog_list:
                    (msg, success) = bot_msgcheck.getMsgSend(content)
                else:
                    msg = '你不是我的master!'
                    success = False
                if success:
                    for group_id in bot_global.group_total_list:
                        try:
                            bot.send_group_msg(group_id=group_id, message=msg)
                        except:
                            reply(bot, context, '群号%s出现发送异常' % group_id, atPeople=False)
                else:
                    reply(bot, context, msg, atPeople=False)

        # 主群超限检测
        if context['message_type'] == 'group' and context['group_id'] in bot_global.group_main_list:
            if not bot_superstar.ignoreUserCheck(bot, context):
                bot_global.sql_action_lock.acquire()
                (out_pp, max_pp, step_pp) = bot_superstar.maxPPCheck(context['group_id'])
                now_user_info = bot_osu.searchUserInfo(context['user_id'], update=False)
                bot_global.sql_action_lock.release()
                msg = ''
                if not now_user_info['sql']:
                    msg = '请绑定本bot以便获取更好的服务\n指令格式为!myid x (x为您的osu!账号)'
                elif not now_user_info['uid']:
                    pass
                elif now_user_info['pp'] < 1:
                    msg = '您的pp低于1,请先进行一次游戏'
                elif now_user_info['pp'] > out_pp:
                    days = max((max_pp-now_user_info['pp'])//step_pp+1, 1)
                    bot_global.super_star_lock.acquire()
                    msg = bot_superstar.checkout(context['group_id'], context['user_id'], now_user_info['uid'], now_user_info['name'], days)
                    bot_global.super_star_lock.release()
                    bot_global.user_check_in_list.append(context['user_id'])
                    bot_IOfile.write_pkl_data(bot_global.user_check_in_list, 'data/data_check_in_list.pkl')
                else:
                    bot_global.user_check_in_list.append(context['user_id'])
                    bot_IOfile.write_pkl_data(bot_global.user_check_in_list, 'data/data_check_in_list.pkl')
                if msg:
                    reply(bot, context, msg, atPeople=True)


# 验证指令是否有权限
# allowed = {'group': [xxx, xxx, xxx], 'discuss': [xxx, xxx, xxx], 'private': []}
# 如果缺少某键,则默认此键相关的直接禁止;若存在private键,则允许任何人私聊使用
def verify(context, allowed):
    if 'group' in allowed:
        if context['message_type'] == 'group' and context['group_id'] not in allowed['group']:
            return False
    else:
        if context['message_type'] == 'group':
            return False
    if 'discuss' in allowed:
        if context['message_type'] == 'discuss' and context['discuss_id'] not in allowed['discuss']:
            return False
    else:
        if context['message_type'] == 'discuss':
            return False
    if 'private' not in allowed:
        if context['message_type'] == 'private':
            return False
    return True


def getGroupMemberInfo(bot, groupid, memberqq):
    result = bot.get_group_member_info(group_id=groupid, user_id=memberqq)
    if 'user_id' in result:
        return result
    else:
        return {}


# 加上艾特人的CQ头
def addAtPeople(user_qq):
    return '[CQ:at,qq=%s] \n' % user_qq


# 根据不同的消息来源(群、讨论组、私聊),统一进行回复
def reply(bot, context, msg, atPeople=False):
    if context['message_type'] == 'group':
        if atPeople:
            msg = addAtPeople(context['user_id']) + msg
        bot.send_group_msg(group_id=context['group_id'], message=msg)
    elif context['message_type'] == 'discuss':
        if atPeople:
            msg = addAtPeople(context['user_id']) + msg
        bot.send_discuss_msg(discuss_id=context['discuss_id'], message=msg)
    elif context['message_type'] == 'private':
        bot.send_private_msg(user_id=context['user_id'], message=msg)
    else:
        print('未知消息来源!' % context)