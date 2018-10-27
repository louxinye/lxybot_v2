# -*- coding: utf-8 -*-
# 带有参数的部分指令检查系统
import random
import re
from center import bot_global


# 函数功能:!afk指令检查
def afk(group, member, content):
    msg1 = ''
    if content == '!afk':
        return 5, msg1, '5秒'
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
                msg2 = '三十封循'
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
        msg = 'roll了个%s' % num
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


# 函数功能!send功能检查
def getMsgSend(content):
    if content == '!send':
        msg = '你倒是说话呀'
    elif '!send ' in content:
        check_msg = re.match(r'^!send (.*)$', content)
        if check_msg:
            msg = check_msg.group(1)
            if not msg:
                msg = '您的!send指令使用错误'
        else:
            msg = '您的!send指令使用错误'
    else:
        msg = '无法识别,bot猜测您是想使用指令!send x(x为参数)'
    return msg


# 函数功能:!remove指令检查
def remove(content):
    num = -1
    if content == '!remove':
        msg = '您的!remove指令使用错误,格式应当如下\n!remove 群代码(1主群,2分群,等等,可通过!group查看)\n举例: !remove 2\n另外请保证该群中本bot是管理员'
    elif '!remove ' in content:
        check_num = re.match(r'!remove ([1234567])', content)
        if check_num:
            msg = '操作执行成功: 0秒'
            num = int(check_num.group(1)) - 1
        else:
            msg = '您的!remove指令使用错误,格式应当如下\n!remove 群代码(1主群,2分群,等等,可通过!group查看)\n举例: !remove 2\n另外请保证该群中本bot是管理员'
    else:
        msg = '无法识别,bot猜测您是想使用指令!remove x(x为参数)'
    return msg, num


def sendSmoke(content):
    success = 0
    smoke = 0
    qq = 0
    if content == '!smoke':
        msg = '我觉得你在逗我'
    else:
        check_msg = re.match(r'^!smoke\[CQ:at,qq=([1-9][0-9]*)\] ([0-9smhd]*)$', content)
        if check_msg:
            qq = int(check_msg.group(1))
            time = str(check_msg.group(2))
            if not time:
                smoke = 60
                msg = '操作执行成功: %s秒' % smoke
                success = 1
            else:
                check_time = re.findall(r'([1-9][0-9]*[smhd])', time)
                print(check_time)
                get_len = 0
                for single_time in check_time:
                    print(single_time)
                    get_len = get_len + len(single_time)
                    temp_time = int(re.match(r'^([1-9][0-9]*)[smhd]$', single_time).group(1))
                    temp_multy = getTimeMul(str(re.match(r'^[1-9][0-9]*([smhd])$', single_time).group(1)))
                    smoke = smoke + temp_time * temp_multy
                if get_len == len(time):
                    if smoke > 2591940:
                        smoke = 2591940
                    msg = '操作执行成功: %s秒' % smoke
                    success = 1
                else:
                    msg = '时间计算好像出了点问题= ='
        else:
            msg = '您的!smoke指令使用错误'
    return msg, success, qq, smoke


def removeSmoke(content):
    success = 0
    qq = 0
    if content == '!unsmoke':
        msg = '我觉得你在逗我'
    else:
        check_msg = re.match(r'^!unsmoke\[CQ:at,qq=([1-9][0-9]*)\] $', content)
        if check_msg:
            qq = int(check_msg.group(1))
            msg = '操作执行成功: 0秒'
            success = 1
        else:
            msg = '您的!unsmoke指令使用错误'
    return msg, success, qq


def sendKill(bot, list_k, group, content):
    success = True
    check_user = re.match(r'!kill\[CQ:at,qq=([1-9][0-9]*)\] $', content)
    if check_user:
        qq = int(check_user.group(1))
        if qq in bot_global.dog_list:
            return '不许欺负bot权限者!'
        if qq in bot_global.host_list:
            return '不许欺负我!'
        user_info = getGroupMemberInfo(bot, group, qq)
        if user_info and user_info['role'] == 'admin':
            return '不许欺负狗管理!'
        if user_info and user_info['role'] == 'owner':
            return '不许欺负狗群主!'
        for i in range(len(list_k)):
            if group == list_k[i]["group"] and qq == list_k[i]["qq"]:
                success = False
                break
        if success:
            list_k.append({"group": group, "qq": qq, "time": 60})
            msg = '已获得飞机票,现在进入60分钟遗言时间'
        else:
            msg = '这人已经有机票了'
    else:
        msg = '您的!kill指令使用错误'
    return msg


def stopKill(list_k, group, content):
    success = False
    check_user = re.match(r'!stop_k\[CQ:at,qq=([1-9][0-9]*)\] $', content)
    if check_user:
        qq = int(check_user.group(1))
        for i in range(len(list_k)):
            if group == list_k[i]["group"] and qq == list_k[i]["qq"]:
                success = True
                del list_k[i]
                break
        if success:
            msg = '已取消此用户的机票'
        else:
            msg = '此用户没有机票'
    else:
        msg = '您的!stop_k指令使用错误'
    return msg


def getTimeMul(a):
    if a == 'd':
        return 86400
    if a == 'h':
        return 3600
    if a == 'm':
        return 60
    else:
        return 1


def getGroupMemberInfo(bot, groupid, memberqq):
    try:
        result = bot.get_group_member_info(group_id=groupid, user_id=memberqq)
    except:
        return {}
    if 'user_id' in result:
        return result
    else:
        return {}