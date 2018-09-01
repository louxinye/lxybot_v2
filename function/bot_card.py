# -*- coding: utf-8 -*-
import random
import re
import copy
from function import bot_osu
from function import bot_IOfile


rare_name = ['MR', 'UR', 'SR', 'R', 'N']  # 稀有度种类
rare_num = [10, 15, 20, 30, 50]  # 每个稀有度的图鉴数量
rate_pick = [1, 12, 80, 280, 1000]  # 单抽或者11连概率,上限1000
rate_fly = [40, 280, 1000, 1000, 1000]  # 飞机票概率,上限1000
p_pick = [0.000100, 0.000733, 0.003400, 0.006667, 0.014400]  # 每张卡抽到概率
p_fly = [0.004, 0.016, 0.036, 0, 0]  # 每张卡飞到概率
b_first = [1000, 500, 200, 50, 10]  # new卡加分
b_next = [300, 150, 50, 10, 1]  # 强化卡加分
tth_Val = [150, 200, 240, 240]  # 更新打图记录时候,四个mode的tth系数

card_n = ['whirLeeve', 'whirLeeve', 'whirLeeve', 'Sega Hatsumi', 'ChongZi', 'NucleophileAP', 'kss233', 'CappuccinoChino',
          'yiyue2', 'yuanxi123', 'Sardin3', 'Kazami-Menhera', 'LITEON', 'Archer9', 'sakiyi', '1716153665', 'ZkmarsvXiYang',
          'dullwolf', 'Trustless532', 'AllenBerserker', 'zawde', 'osu happy', 'ninler', '00guainiubi', 'xiaoxi654',
          'ojbk', '_Star', 'Game Addiction', 'chan0165', 'HaiTanYangGuang', 'whiteseason2018', 'newplayre', 'KPC123',
          'Against Current', '24fps', '- ElementOp -', 'My Angel-Asher-', 'Tacmyw', 'Dango_YwY', 'Aleafy', 'Sora_w',
          'matco', '[SHIYU]', 'K_vAE', 'Neptsun', 'ink rhyme',
          'cookiezi', 'Rafis', 'Vaxei', 'Emilia', 'Mathi', '-GN']
card_r = ['[ Kuon ]', 'godel', '-Hermit-', 'IaKis', 'ykzl1969497633', 'bleatingsheep', 'akziyou', 'Pixiv', '[mogezi]',
          'GreySTrip', 'sodarose', 'misaki nene', 'kahei0726', 'bilibilicnm', 'yimoQWQ', 'PlaZmAx', 'FelxMy', 'Gust',
          'X_fire233', 'IronWitness', 'SakuraOmega', 'SinowWhite', 'tanwanlanyue', 'Rein_Liya', 'lonelyling', '-NekoMinto-',
          'CoCo-OuO', 'wdwdwww', 'DalouBot', '[ morion ]']
card_sr = ['KA MI NA', 'Cookeazy', 'ShiQiKuangSanzz', 'Truth you left', '-Inui Sana-', 'Mindlessness', 'Arcareh', 'Aok',
           'BiliBiliZyi', 'COOLMILK123', 'GAddict', 'DePuppy', 'C8N16O32' , '-inter-', '-Q', 'usagiKokoa', '-FKai-',
           'Hanasaki Yukina', 'orangeLief', 'Sakura miku']
card_ur = ['taolex',  'Sonoaoi', 'Kutouzi', '-Artemis', 'AdorableCubCat', 'ye__ow', 'Mafuyu Shiina', 'zfxggg',
           'Fushimi Rio', 'Sisters10086', 'my angel kotori', 'dicskb122', 'heisiban',
           'AyaSakura', 'Imouto koko']
card_mr = ['PandaCattle', '84461810', 'Aero-zero', 'Jack_Wang_', 'bless_von', 'TuGuanZ', 'Firika', 'Hibikom', 'Pata-Mon',
           'Sayori_yui']
card_next = []


# 注册并开始活动
def startCard(card_member, list_c, content):
    for member in list_c:
        if card_member == member['qq']:
            msg = '此QQ号已被注册,活动进行中'
            return msg
    if content == '!start_card':
        msg = '倒是告诉我id啊'
    elif '!start_card ' in content:
        check_id = re.match(r'^!start_card (.*)$', content)
        if check_id:
            osu_name = check_id.group(1)
            osu_id = '0'
            real_name = '0'
            pc = [0, 0, 0, 0]
            tth = [0, 0, 0, 0]
            medal = [0, 0, 0, 0, 0, 0, 0]
            for i in range(4):
                (osu_id, real_name, pp, pc[i], tth[i], acc) = bot_osu.getUserInfo(osu_name, i)
                if not osu_id:
                    msg = '查询失败,可能为输入错误或网络延迟'
                    return msg
            money = 100
            user_info = {'qq': card_member, 'uid': osu_id, 'name': real_name, 'pc': pc, 'tth': tth, 'money': money,
                         'fly': 0, 'card': [[], [], [], [], []], 'pt': 0, 'total_money': money, 'boom_money': 0,
                         'boom_cost': 30, 'bonus_pt': 0, 'medal': medal, 'lucky': 0, 'lucky_rate': 0}
            msg = '玩家信息:\nqq号: %s\nuid: %s\nname: %s\npc: %s\ntth: %s\nmoney: %s\n机票数: 0\n活动开始!'\
                  % (card_member, osu_id, real_name, pc, tth, money)
            list_c.append(user_info)
            bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
        else:
            msg = '您的!start_card指令使用错误'
    else:
        msg = '无法识别,bot猜测您是想使用指令!start_card x (x为参数)'
    return msg


# 取消某人的活动
def stopCard(list_c, content):
    if content == '!ban_card':
        msg = '倒是告诉我qq号啊'
    elif '!ban_card ' in content:
        check_qq = re.match(r'^!ban_card ([123456789][0123456789]*)$', content)
        if check_qq:
            qq = int(check_qq.group(1))
            for i in range(len(list_c)):
                if list_c[i]['qq'] == qq:
                    del list_c[i]
                    bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
                    msg = '已删除此qq号活动数据'
                    return msg
            msg = '该qq号并没有参加活动'
        else:
            msg = '您的!ban_card指令使用错误'
    else:
        msg = '无法识别,bot猜测您是想使用指令!ban_card x (x为参数)'
    return msg


# 查看本QQ号的目前活动信息
def userGameInfo(card_member, list_c):
    for member in list_c:
        if card_member == member['qq']:
            msg = '玩家活动信息:\nname: %s\n记录在案的pc: %s\n记录在案的tth: %s\nmoney: %s\n机票数: %s\n总金币: %s\n活动pt: %s'\
                  % (member['name'], member['pc'], member['tth'], member['money'], flyNumCal(member['fly']), member['total_money'], member['pt'])
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 查看本QQ号的目前图鉴信息
def userCardInfo(card_member, list_c):
    for member in list_c:
        if card_member == member['qq']:
            card_list = member['card']
            msg = '玩家已得到的卡:'
            for rare_code in range(5):
                msg = msg + '\n【%s系列】图鉴解锁%s/%s' % (rare_name[rare_code], len(card_list[rare_code]), rare_num[rare_code])
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 查看本QQ号的目前抽卡信息
def userCardDetail(member_qq, list_c, rare_code, contact='group'):
    if contact != 'private':
        msg = '请私聊查询'
        return msg
    for member in list_c:
        if member_qq == member['qq']:
            card_list = member['card']
            if not len(card_list[rare_code]):
                msg = '此玩家抽到的%s系列卡……这么伤心的事不忍心说啊' % rare_name[rare_code]
            else:
                msg = '【%s系列】图鉴解锁%s/%s' % (rare_name[rare_code], len(card_list[rare_code]), rare_num[rare_code])
                for card in card_list[rare_code]:
                    msg = msg + '\n%s (%s)' % (card['card_name'], card['card_number'])
                msg = msg + '\n括号内数字代表数量'
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 查看本QQ号的目前成就信息
def userMedalDetail(card_member, list_c):
    for member in list_c:
        if card_member == member['qq']:
            medal_list = member['medal']
            msg = '成就完成进度:'
            msg = msg + '\n稀有MR卡全收集: %s%%' % medal_list[0]
            msg = msg + '\n稀有UR卡全收集: %s%%' % medal_list[1]
            msg = msg + '\nSR卡全收集: %s%%' % medal_list[2]
            msg = msg + '\nR卡全收集: %s%%' % medal_list[3]
            msg = msg + '\nN卡全收集: %s%%' % medal_list[4]
            msg = msg + '\n水王之王: %s%%' % medal_list[5]
            msg = msg + '\n天命之子: %s%%' % medal_list[6]
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 查看本QQ号的目前排名信息
def userRank(card_member, list_c):
    list_card = copy.deepcopy(list_c)
    list_card.sort(key=lambda x: x['total_money'], reverse=True)
    for i in range(len(list_card)):
        if card_member == list_card[i]['qq']:
            msg = '排名信息如下:\nname: %s\n金币榜: 第%s名 (%s)\n' % (list_card[i]['name'], i+1, list_card[i]['total_money'])
            list_card.sort(key=lambda x: x['pt'], reverse=True)
            for j in range(len(list_card)):
                if card_member == list_card[j]['qq']:
                    lucky_msg = '%.2f (期望%s)' % (float(list_card[j]['lucky_rate']), list_card[j]['lucky'])
                    msg = msg + 'pt榜: 第%s名 (%s)\n欧皇系数: %s\n总人数: %s' % (j + 1, list_card[j]['pt'], lucky_msg, len(list_card))
                    return msg
    msg = '此玩家并未参与活动'
    return msg


# 查看某用户名的目前图鉴信息,一般用于他人查询
def otherCardInfo(list_c, content):
    if content == '!card':
        msg = '你倒是告诉我要查谁啊'
        return msg
    if '!card ' in content:
        check_name = re.match(r'^!card (.*)$', content)
        if check_name:
            osu_name = check_name.group(1)
            for member in list_c:
                if osu_name == member['name']:
                    card_list = member['card']
                    msg = '玩家已得到的卡:'
                    for rare_code in range(5):
                        msg = msg + '\n【%s系列】图鉴解锁%s/%s' % (rare_name[rare_code], len(card_list[rare_code]), rare_num[rare_code])
                    return msg
            msg = '此玩家并未参与活动'
        else:
            msg = '您的!card指令使用错误'
    else:
        msg = '无法识别，bot猜测您是想使用指令!card x (x为参数)'
    return msg


# 查看某用户名的目前排名信息,一般用于他人查询
def otherRank(list_c, content):
    list_card = copy.deepcopy(list_c)
    if content == '!rank':
        msg = '你倒是告诉我要查谁啊'
        return msg
    if '!rank ' in content:
        check_name = re.match(r'!rank (.*)', content)
        if check_name:
            osu_name = check_name.group(1)
            list_card.sort(key=lambda x: x['total_money'], reverse=True)
            for i in range(len(list_card)):
                if osu_name == list_card[i]['name']:
                    msg = '排名信息如下:\nname: %s\n金币榜: 第%s名 (%s)\n' % (list_card[i]['name'], i+1, list_card[i]['total_money'])
                    list_card.sort(key=lambda x: x['pt'], reverse=True)
                    for j in range(len(list_card)):
                        if osu_name == list_card[j]['name']:
                            lucky_msg = '%.2f (期望%s)' % (float(list_card[j]['lucky_rate']), list_card[j]['lucky'])
                            msg = msg + 'pt榜: 第%s名 (%s)\n欧皇系数: %s\n总人数: %s' % (j + 1, list_card[j]['pt'], lucky_msg, len(list_card))
                            return msg
            msg = '此玩家并未参与活动'
        else:
            msg = '您的!rank指令使用错误'
    else:
        msg = '无法识别，bot猜测您是想使用指令!rank x (x为参数)'
    return msg


# 计算已抽到的卡库中全部卡的数量
def totalCardNum(card_set):
    num = 0
    for i in range(5):
        for card in card_set[i]:
            num = num + card['card_number']
    return num


# 针对一条user记录，进行打图信息更新
def GameUpdate(user):
    osu_uid = user['uid']
    osu_name = user['name']
    update_success = True
    update_success_detail = [1, 1, 1, 1]
    pc = [0, 0, 0, 0]
    tth = [0, 0, 0, 0]
    add_money = 0
    for i in range(4):
        (osu_id, name, pp, pc[i], tth[i], acc) = bot_osu.getUserInfo(osu_uid, i, type_mode='id')
        if not osu_id:
            print('%s的mode%s查询失败' % (osu_name, i))
            pc[i] = user['pc'][i]
            tth[i] = user['tth'][i]
            update_success = False
            update_success_detail[i] = 0
        else:
            osu_name = name
            print('%s的mode%s查询成功' % (osu_name, i))
            add_money = add_money + (pc[i] - user['pc'][i]) + (tth[i] - user['tth'][i]) // tth_Val[i]
    user['name'] = osu_name
    user['pc'] = pc
    user['tth'] = tth
    user['money'] = user['money'] + add_money
    user['total_money'] = user['total_money'] + add_money
    msg = '更新打图信息:\nname: %s\nmoney: %s (+%s)\n机票数: %s\n总金币: %s (+%s)\n活动pt: %s' \
          % (user['name'], user['money'], add_money, flyNumCal(user['fly']), user['total_money'], add_money, user['pt'])
    if not update_success:
        msg = msg + '\n注意,您有部分mode查询失败,因此下列数据没有更新:'
        for j in range(4):
            if not update_success_detail[j]:
                msg = msg + ' %s' % bot_osu.getMode(j)
    return user, msg, update_success, update_success_detail


# 针对本QQ号进行打图信息更新
def oneUserUpdate(card_member, list_c):
    for i in range(len(list_c)):
        member = list_c[i]
        if card_member == member['qq']:
            (list_c[i], msg, update_success, update_success_detail) = GameUpdate(member)
            bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 针对指定玩家进行打图信息更新
def certainUserUpdate(list_c, content):
    check_name = re.match(r'^!update (.*)$', content)
    if check_name:
        osu_name = check_name.group(1)
        for i in range(len(list_c)):
            member = list_c[i]
            if osu_name == member['name']:
                (list_c[i], msg, success, success_detail) = GameUpdate(member)
                bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
                return msg
        msg = '此玩家并未参与活动'
    else:
        msg = '您的!update指令使用错误'
    return msg


# 针对全体参与者进行打图信息更新
def allUserUpdate(list_c):
    error_list = []
    error_detail = []
    for i in range(len(list_c)):
        member = list_c[i]
        (list_c[i], msg, update_success, update_success_detail) = GameUpdate(member)
        if not update_success:
            error_list.append(member['name'])
            error_detail.append(update_success_detail)
            print('%s. 完成%s, 失败' % (i+1, member['name']))
        else:
            print('%s. 完成%s, 成功' % (i+1, member['name']))
    bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
    if not error_list:
        msg = '全体打图记录更新完毕,没有发生错误'
    else:
        msg = '下列玩家由于延迟爆炸查询失败:'
        for i in range(len(error_list)):
            msg = msg + '\n%s:' % error_list[i]
            for j in range(4):
                if not error_detail[i][j]:
                    msg = msg + ' %s' % bot_osu.getMode(j)
    return msg


# 单抽
def pick1(card_member, list_c):
    for i in range(len(list_c)):
        if card_member == list_c[i]['qq']:
            if list_c[i]['money'] < 10:
                msg = '金币数量低于10! 快去打图'
            else:
                list_c[i]['money'] = list_c[i]['money'] - 10
                msg = '单抽结果:'
                card_set = list_c[i]['card']
                (rare_code, new_card) = choose()
                existence = 0
                for j2 in range(len(card_set[rare_code])):
                    if new_card == card_set[rare_code][j2]['card_name']:
                        existence = 1
                        msg = msg + '\n%s: %s' % (rare_name[rare_code], new_card)
                        card_set[rare_code][j2]['card_number'] = card_set[rare_code][j2]['card_number'] + 1
                        break
                if existence == 0:
                    msg = msg + '\n%s: %s (new!)' % (rare_name[rare_code], new_card)
                    card_set[rare_code].append({'card_name': new_card, 'card_number': 1})
                new_unlock = medalUnlock(card_set)
                if list_c[i]['medal'][6] == 100:
                    new_unlock[6] = 100
                new_pt = check_pt(card_set, list_c[i]['bonus_pt'], new_unlock)
                medal_msg = medalUpdate(list_c[i]['medal'], new_unlock)
                msg = msg + '\n金币数变更: %s → %s' % (list_c[i]['money']+10, list_c[i]['money'])
                msg = msg + '\n机票数变更: %s → %s' % (flyNumCal(list_c[i]['fly']), flyNumCal(list_c[i]['fly']+1))
                msg = msg + '\n活动pt变更: %s → %s' % (list_c[i]['pt'], new_pt)
                if medal_msg:
                    msg = msg + '\n解锁隐藏成就:' + medal_msg
                list_c[i]['fly'] = list_c[i]['fly'] + 1
                list_c[i]['card'] = card_set
                list_c[i]['pt'] = new_pt
                list_c[i]['medal'] = new_unlock
                (lucky, lucky_rate) = European(list_c[i])
                list_c[i]['lucky'] = lucky
                list_c[i]['lucky_rate'] = lucky_rate
                bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 11连
def pick11(card_member, list_c):
    for i in range(len(list_c)):
        if card_member == list_c[i]['qq']:
            if list_c[i]['money'] < 100:
                msg = '金币数量低于100! 快去打图'
            else:
                list_c[i]['money'] = list_c[i]['money'] - 100
                msg = '11连结果:'
                card_set = list_c[i]['card']
                getR = False  # 这一轮11连是不是抽到了R或以上
                for times in range(11):
                    (rare_code, new_card) = choose()
                    getNew = True
                    if rare_code < 4:
                        getR = True
                    for j in range(len(card_set[rare_code])):
                        if new_card == card_set[rare_code][j]['card_name']:
                            getNew = False
                            msg = msg + '\n%s: %s' % (rare_name[rare_code], new_card)
                            card_set[rare_code][j]['card_number'] = card_set[rare_code][j]['card_number'] + 1
                            break
                    if getNew:
                        msg = msg + '\n%s: %s (new!)' % (rare_name[rare_code], new_card)
                        card_set[rare_code].append({'card_name': new_card, 'card_number': 1})
                new_unlock = medalUnlock(card_set)
                if list_c[i]['medal'][6] == 100 or not getR:
                    new_unlock[6] = 100
                new_pt = check_pt(card_set, list_c[i]['bonus_pt'], new_unlock)
                medal_msg = medalUpdate(list_c[i]['medal'], new_unlock)
                msg = msg + '\n金币数变更: %s → %s' % (list_c[i]['money'] + 100, list_c[i]['money'])
                msg = msg + '\n机票数变更: %s → %s' % (flyNumCal(list_c[i]['fly']), flyNumCal(list_c[i]['fly'] + 10))
                msg = msg + '\n活动pt变更: %s → %s' % (list_c[i]['pt'], new_pt)
                if medal_msg:
                    msg = msg + '\n解锁隐藏成就:' + medal_msg
                list_c[i]['fly'] = list_c[i]['fly'] + 10
                list_c[i]['card'] = card_set
                list_c[i]['pt'] = new_pt
                list_c[i]['medal'] = new_unlock
                (lucky, lucky_rate) = European(list_c[i])
                list_c[i]['lucky'] = lucky
                list_c[i]['lucky_rate'] = lucky_rate
                bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 全抽
def pickall(card_member, list_c):
    for i in range(len(list_c)):
        if card_member == list_c[i]['qq']:
            if list_c[i]['money'] < 100:
                msg = '金币数量低于100! 快去打图'
            else:
                num_all = [0, 0, 0, 0, 0]
                num_new = [0, 0, 0, 0, 0]
                pick_time = list_c[i]['money'] // 100
                list_c[i]['money'] = list_c[i]['money'] - pick_time * 100
                msg = '%s次11连结果:' % pick_time
                card_set = list_c[i]['card']
                this_getR = False  # 这一轮11连是不是抽到了R以上
                total_getR = True  # 这次全抽是不是有一轮抽到了R以上
                for times in range(pick_time * 11):
                    if times % 11 == 0:
                        this_getR = False
                    (rare_code, new_card) = choose()
                    if rare_code < 4:
                        this_getR = True
                    if times % 11 == 10 and not this_getR:
                        total_getR = False
                    num_all[rare_code] = num_all[rare_code] + 1
                    getNew = True
                    for j in range(len(card_set[rare_code])):
                        if new_card == card_set[rare_code][j]['card_name']:
                            getNew = False
                            card_set[rare_code][j]['card_number'] = card_set[rare_code][j]['card_number'] + 1
                            break
                    if getNew:
                        num_new[rare_code] = num_new[rare_code] + 1
                        card_set[rare_code].append({'card_name': new_card, 'card_number': 1})
                for xx in range(5):
                    msg = msg + '\n【%s系列】获得%s(%s)张卡' % (rare_name[xx], num_all[xx], num_new[xx])
                msg = msg + '\n括号内数字代表图鉴新解锁数量'
                new_unlock = medalUnlock(card_set)
                if list_c[i]['medal'][6] == 100 or not total_getR:
                    new_unlock[6] = 100
                new_pt = check_pt(card_set, list_c[i]['bonus_pt'], new_unlock)
                medal_msg = medalUpdate(list_c[i]['medal'], new_unlock)
                msg = msg + '\n金币数变更: %s → %s' % (list_c[i]['money']+pick_time*100, list_c[i]['money'])
                msg = msg + '\n机票数变更: %s → %s' % (flyNumCal(list_c[i]['fly']), flyNumCal(list_c[i]['fly']+pick_time*10))
                msg = msg + '\n活动pt变更: %s → %s' % (list_c[i]['pt'], new_pt)
                if medal_msg:
                    msg = msg + '\n解锁隐藏成就:' + medal_msg
                list_c[i]['fly'] = list_c[i]['fly'] + pick_time * 10
                list_c[i]['card'] = card_set
                list_c[i]['pt'] = new_pt
                list_c[i]['medal'] = new_unlock
                (lucky, lucky_rate) = European(list_c[i])
                list_c[i]['lucky'] = lucky
                list_c[i]['lucky_rate'] = lucky_rate
                bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 飞机票
def fly1(card_member, list_c):
    for i in range(len(list_c)):
        if card_member == list_c[i]['qq']:
            if list_c[i]['fly'] < 50:
                msg = '机票数量低于5! 快去抽卡'
            else:
                list_c[i]['fly'] = list_c[i]['fly'] - 50
                msg = '偷渡结果:'
                card_set = list_c[i]['card']
                (rare_code, new_card) = choose_fly()
                getNew = True
                for j in range(len(card_set[rare_code])):
                    if new_card == card_set[rare_code][j]['card_name']:
                        getNew = False
                        msg = msg + '\n%s: %s' % (rare_name[rare_code], new_card)
                        card_set[rare_code][j]['card_number'] = card_set[rare_code][j]['card_number'] + 1
                        break
                if getNew:
                    msg = msg + '\n%s: %s (new!)' % (rare_name[rare_code], new_card)
                    card_set[rare_code].append({'card_name': new_card, 'card_number': 1})
                new_unlock = medalUnlock(card_set)
                if list_c[i]['medal'][6] == 100:
                    new_unlock[6] = 100
                new_pt = check_pt(card_set, list_c[i]['bonus_pt'], new_unlock)
                medal_msg = medalUpdate(list_c[i]['medal'], new_unlock)
                msg = msg + '\n机票数变更: %s → %s' % (flyNumCal(list_c[i]['fly'] + 50), flyNumCal(list_c[i]['fly']))
                msg = msg + '\n活动pt变更: %s → %s' % (list_c[i]['pt'], new_pt)
                if medal_msg:
                    msg = msg + '\n解锁隐藏成就:' + medal_msg
                list_c[i]['card'] = card_set
                list_c[i]['pt'] = new_pt
                list_c[i]['medal'] = new_unlock
                (lucky, lucky_rate) = European(list_c[i])
                list_c[i]['lucky'] = lucky
                list_c[i]['lucky_rate'] = lucky_rate
                bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 单抽实现
def choose():
    i = random.randint(0,999)
    if i < rate_pick[0]:
        return 0, random.choice(card_mr)
    elif i < rate_pick[1]:
        return 1, random.choice(card_ur)
    elif i < rate_pick[2]:
        return 2, random.choice(card_sr)
    elif i < rate_pick[3]:
        return 3, random.choice(card_r)
    else:
        return 4, random.choice(card_n)


# 飞机票实现
def choose_fly():
    i = random.randint(0, 999)
    if i < rate_fly[0]:
        return 0, random.choice(card_mr)
    elif i < rate_fly[1]:
        return 1, random.choice(card_ur)
    elif i < rate_fly[2]:
        return 2, random.choice(card_sr)
    elif i < rate_fly[3]:
        return 3, random.choice(card_r)
    else:
        return 4, random.choice(card_n)


# 根据卡库和成就进度计算该玩家的活动pt
def check_pt(card_set, bonus, new_unlock):
    pt = bonus
    for card in card_set[0]:
        pt = pt + 700 + 300 * card['card_number']
    for card in card_set[1]:
        pt = pt + 350 + 150 * card['card_number']
    for card in card_set[2]:
        pt = pt + 150 + 50 * card['card_number']
    for card in card_set[3]:
        pt = pt + 40 + 10 * card['card_number']
    for card in card_set[4]:
        pt = pt + 9 + 1 * card['card_number']
    for rate in new_unlock:
        if rate >= 100:
            pt = pt + 1000
    return pt


# 检查是否有新成就解锁
def medalUpdate(old_unlock, new_unlock):
    medal_list = []
    msg = ''
    if old_unlock[0] < 100 and new_unlock[0] >= 100:
        medal_list.append('稀有MR卡全收集')
    if old_unlock[1] < 100 and new_unlock[1] >= 100:
        medal_list.append('稀有UR卡全收集')
    if old_unlock[2] < 100 and new_unlock[2] >= 100:
        medal_list.append('SR卡全收集')
    if old_unlock[3] < 100 and new_unlock[3] >= 100:
        medal_list.append('R卡全收集')
    if old_unlock[4] < 100 and new_unlock[4] >= 100:
        medal_list.append('N卡全收集')
    if old_unlock[5] < 100 and new_unlock[5] >= 100:
        medal_list.append('水王之王')
    if old_unlock[6] < 100 and new_unlock[6] >= 100:
        medal_list.append('天命之子')
    if medal_list:
        for medal in medal_list:
            msg = msg + ' ☆%s' % medal
    return msg


# 成就进度统计: 稀有MR,稀有UR,全体R,全体R,全体N,指定N,全N
def medalUnlock(card_set):
    unlock = [0, 0, 0, 0, 0, 0, 0]
    for i in range(2, 5):
        if len(card_set[i]) >= rare_num[i]:
            unlock[i] = 100
        else:
            unlock[i] = (100 * len(card_set[i])) // rare_num[i]
    for card in card_set[0]:
        if card['card_name'] == 'Pata-Mon':
            unlock[0] = 100
    for card in card_set[1]:
        if card['card_name'] == 'AyaSakura':
            unlock[1] = unlock[1] + 50
        if card['card_name'] == 'Imouto koko':
            unlock[1] = unlock[1] + 50
    for card in card_set[4]:
        if card['card_name'] == 'whirLeeve':
            if card['card_number'] >= 30:
                unlock[5] = 100
            else:
                unlock[5] = (100 * card['card_number']) // 30
    return unlock


# 欧洲系数计算
def European(user):
    use_money = max(0, user['total_money'] - user['money'] - user['boom_money'])
    num_fly = max(0, (use_money // 10 - user['fly']) // 50)
    num_pick = max(0, totalCardNum(user['card']) - num_fly)
    if num_pick == 0:
        return 0, 0
    # 成就加分，因为不好计算因此只是简单估计
    if use_money > 16000:
        e_pt = 6000
    elif use_money > 7000:
        e_pt = 3000 + (use_money - 7000) // 3
    elif use_money > 4000:
        e_pt = 1000 + (use_money - 4000) // 1.5
    elif use_money > 2000:
        e_pt = (use_money - 2000) // 2
    else:
        e_pt = 0
    for i in range(5):
        p_have = 1 - ((1 - p_pick[i]) ** num_pick) * ((1 - p_fly[i]) ** num_fly)
        e_have = p_pick[i] * num_pick + p_fly[i] * num_fly
        e_pt = e_pt + (p_have * b_first[i] + (e_have - p_have) * b_next[i]) * rare_num[i]
    european_pt = int(e_pt)
    european_rate = user['pt'] / european_pt
    return european_pt, european_rate


# 输出全体玩家排名情况
def rankAll(list_c, keyVal, contact='group'):
    list_card = copy.deepcopy(list_c)
    if contact == 'private':
        maxnum = 15
    else:
        maxnum = 5
    member_number = min(len(list_card), maxnum)
    if keyVal == 'pt_down':
        list_card.sort(key=lambda x: x['pt'], reverse=True)
        msg = 'pt排行榜(正序):'
        for i in range(member_number):
            msg = msg + '\n%s: %s (%s)' % (i+1, list_card[i]['name'], list_card[i]['pt'])
    elif keyVal == 'pt_up':
        list_card.sort(key=lambda x: x['pt'], reverse=False)
        msg = 'pt排行榜(倒序):'
        for i in range(member_number):
            msg = msg + '\n%s: %s (%s)' % (i + 1, list_card[i]['name'], list_card[i]['pt'])
    elif keyVal == 'mn_down':
        list_card.sort(key=lambda x: x['total_money'], reverse=True)
        msg = '总金币排行榜(正序):'
        for i in range(member_number):
            msg = msg + '\n%s: %s (%s)' % (i+1, list_card[i]['name'], list_card[i]['total_money'])
    elif keyVal == 'mn_up':
        list_card.sort(key=lambda x: x['total_money'], reverse=False)
        msg = '总金币排行榜(倒序):'
        for i in range(member_number):
            msg = msg + '\n%s: %s (%s)' % (i + 1, list_card[i]['name'], list_card[i]['total_money'])
    else:
        list_lucky = []
        for user in list_card:
            if totalCardNum(user['card']) > 99:
                list_lucky.append({'lucky': user['lucky_rate'], 'name': user['name']})
        member_number = min(len(list_lucky), maxnum)
        if keyVal == 'lucky_down':
            list_lucky.sort(key=lambda x: x['lucky'], reverse=True)
            msg = '欧皇排行榜(正序):'
            for i in range(member_number):
                msg = msg + '\n%s: %s (%.2f)' % (i+1, list_lucky[i]['name'], list_lucky[i]['lucky'])
            msg = msg + '\n有效人数(抽100张卡): %s' % len(list_lucky)
        else:
            list_lucky.sort(key=lambda x: x['lucky'], reverse=False)
            msg = '欧皇排行榜(倒序):'
            for i in range(member_number):
                msg = msg + '\n%s: %s (%.2f)' % (i + 1, list_lucky[i]['name'], list_lucky[i]['lucky'])
            msg = msg + '\n有效人数(抽100张卡): %s' % len(list_lucky)
    msg = msg + '\n请大家继续加油!'
    return msg


# 为了不出错,机票数量是乘以10存储的(整型),实际显示需要除以10
def flyNumCal(a):
    t = a % 10
    if not t:
        msg = '%d' % (a/10)
    else:
        msg = '%.1f' % (a/10)
    return msg


def gailv():
    txt = '''DalouCard抽卡概率公布

单抽or11连
MR: 0.1%
UR: 1.1%
SR: 6.8%
R: 20%
N: 72%
飞机票偷渡
MR: 4%
UR: 24%
SR: 72%
【注1】11连无保底
【注2】绝大部分同稀有度卡的抽取概率相等,少数卡除外
【注3】抽卡不存在产出控制和仓库检测'''
    return txt


def jiazhi():
    txt = '''DalouCard卡牌价值公布

MR: 1000(300)
UR: 500(150)
SR: 200(50)
R: 50(10)
N: 10(1)
括号内数字代表卡牌每强化1级的增加量'''
    return txt


# 测试指令,加1000金币
def addMoney(card_member, list_c):
    for i in range(len(list_c)):
        if card_member == list_c[i]['qq']:
            list_c[i]['money'] = list_c[i]['money'] + 1000
            bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
            msg = '金币+1000'
            return msg
    msg = '此玩家并未参与活动'
    return msg


# 爆炸指令
def sendBoom(list_c, card_member, content):
    success = 0
    smoke1 = 0
    smoke2 = 0
    qq = 0
    if content == '!boom':
        msg = '我觉得你在逗我(指令最后需要紧跟着艾特一个人)'
        return msg, success, qq, smoke1, smoke2
    for i in range(len(list_c)):
        if card_member == list_c[i]['qq']:
            now_boom_money = list_c[i]['boom_cost']
            if list_c[i]['money'] < now_boom_money:
                msg = '金币数量低于%s! 快去打图' % now_boom_money
            else:
                check_msg = re.match(r'^!boom\[CQ:at,qq=([1-9][0-9]*)\]', content)
                if check_msg:
                    list_c[i]['money'] = list_c[i]['money'] - now_boom_money
                    list_c[i]['boom_money'] = list_c[i]['boom_money'] + now_boom_money
                    list_c[i]['boom_cost'] = list_c[i]['boom_cost'] + 2
                    bot_IOfile.write_pkl_data(list_c, 'data/data_card_game_list.pkl')
                    qq = int(check_msg.group(1))
                    smoke2 = random.randint(30, 100)
                    smoke1 = int(smoke2 * random.uniform(0.5, 3))
                    msg = '操作执行成功\n对方: %s秒, 自己: %s秒\n金币变更情况: %s → %s\n炸弹购买价格: %s → %s' \
                          % (smoke1, smoke2, list_c[i]['money']+now_boom_money, list_c[i]['money'], list_c[i]['boom_cost']-2, list_c[i]['boom_cost'])
                    success = 1
                else:
                    msg = '您的!boom指令使用错误(指令最后需要紧跟着艾特一个人)'
            return msg, success, qq, smoke1, smoke2
    msg = '此玩家并未参与活动'
    return msg, success, qq, smoke1, smoke2