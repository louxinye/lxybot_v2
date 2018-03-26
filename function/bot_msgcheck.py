# -*- coding: utf-8 -*-
# 带有参数的部分指令检查系统
import random
import re


# 函数功能:!afk指令检查
def afk(group, member, content):
    msg1 = ''
    if content == '!afk':
        return 5, msg1, 0
    elif '!afk ' in content:
        check_num = re.match(r'^!afk ([123456789][0123456789]*)([smhd])$', content)
        if check_num:
            ban_time = int(check_num.group(1))
            ban_type = check_num.group(2)
            if ban_type == 'd':
                smoke = ban_time * 86400
                msg2 = '%s天' % ban_time
            elif ban_type == 'h':
                smoke = ban_time * 3600
                msg2 = '%s小时' % ban_time
            elif ban_type == 'm':
                smoke = ban_time * 60
                msg2 = '%s分' % ban_time
            else:
                smoke = ban_time * 1
                msg2 = '%s秒' % ban_time
            if smoke > 2591940:
                smoke = 2591940
            return smoke, msg1, msg2
        else:
            msg1 = '您的!afk指令使用错误'
    else:
        msg1 = '无法识别,bot猜测您是想使用指令!afk x (x为参数,缺省值5s)'
    return 0, msg1, 0


# 函数功能:!roll指令检查
def roll(content):
    if content == '!roll':
        num = random.randint(1, 100)
        msg = 'roll了一个%s' % num
    elif '!roll ' in content:
        check_roll = re.match(r'^!roll ([123456789][0123456789]*$)', content)
        if check_roll:
            roll_max = int(check_roll.group(1))
            if roll_max > 100000:
                msg = '参数过大'
            else:
                num = random.randint(1, roll_max)
                msg = 'roll了个%s' % num
        else:
            msg = '您的!roll指令使用错误'
    else:
        msg = '无法识别,bot猜测您是想使用指令!roll x (x为参数,缺省值100)'
    return msg


'''
# 函数功能:!kill指令检查
def kill(list_k, list_g, list_d,  group, content):
    success = 1
    check_user = re.match(r'!kill@(.*) ', content)
    if check_user:
        card = check_user.group(1)
        gl = bot.List('group', group)
        if gl:
            group1 = gl[0]
            member1 = bot.List(group1, card)
            if member1:
                for i in range(len(list_k)):
                    if group == list_k[i]["group"] and member1[0].qq == list_k[i]["qq"]:
                        success = 0
                        break
                if member1[0].qq in list_g or member1[0].qq in list_d:
                    msg = '你在搞笑吗'
                elif success == 1:
                    list_k.append({"group": group, "qq": member1[0].qq, "time": 60})
                    msg = '已获得飞机票,现在进入60分钟遗言时间'
                else:
                    msg = '这人已经有机票了'
            else:
                msg = '找不到此人信息'
        else:
            msg = '找不到群组信息'
    else:
        msg = '您的!kill指令使用错误'
    return list_k, msg


# 函数功能:!stop_k指令检查
def stop_k(list_k, group, content):
    success = 0
    check_user = re.match(r'!stop_k@(.*) ', content)
    if check_user:
        card = check_user.group(1)
        gl = bot.List('group', group)
        if gl:
            group1 = gl[0]
            member1 = bot.List(group1, card)
            if member1:
                for i in range(len(list_k)):
                    if group == list_k[i]["group"] and member1[0].qq == list_k[i]["qq"]:
                        del list_k[i]
                        success = 1
                        break
                if success == 0:
                    msg = '这人并没有机票'
                else:
                    msg = '已经取消此人的机票'
            else:
                msg = '找不到此人信息'
        else:
            msg = 'bot遇到了奇怪的错误!'
    else:
        msg = '您的!stop_k指令使用错误'
    return list_k, msg
'''


# 函数功能:!remove指令检查
def remove(content):
    num = -1
    if content == '!remove':
        msg = '您的!remove指令使用错误,格式应当如下\n!remove 群代码(1主群,2分群,等等)\n举例: !remove 2'
    elif '!remove ' in content:
        check_num = re.match(r'!remove ([123456])', content)
        if check_num:
            msg = '操作执行成功: 0秒'
            num = int(check_num.group(1)) - 1
        else:
            msg = '您的!remove指令使用错误,格式应当如下\n!remove 群代码(1主群,2分群,等等)\n举例: !remove 2'
    else:
        msg = '无法识别,bot猜测您是想使用指令!remove x(x为参数)'
    return msg, num
