# -*- coding: utf-8 -*-
# 函数功能:查看各类帮助文档或者列表
import copy
from center import bot_global


def getHelp():
    txt = '''发烟bot使用说明

!group  查看适用群
!roll   随机取数(可选参数)
!myid   绑定id
!mypp   速查信息
!myrct  查询最新游戏记录
!mylevel 查询评价
!欢送系统
!抽烟系统
!找图系统
!健康系统
!监视系统
!咩羊游戏
!月常活动
!chart活动
!dog   查询bot权限者
!kill  查询踢人列表
帮助文档 https://github.com/louxinye/lxybot_v2/wiki
v3.00 关服版'''
    return txt


def smokeSystem():
    txt = '''抽烟系统介绍

☆!cnm    5-100秒娱乐套餐
☆!rest   1小时休息套餐
☆!sleep  6小时睡眠套餐
☆!afk    闭群套餐(可选参数,形式为<num><type>,例如3d等于3天)
☆!remove 私聊解禁(关闭)
注意事项
本系统效果为主动让自己禁言,适合那些控制不住自己水群的孩子使用'''
    return txt


def farewellSystem():
    txt = '''欢送系统介绍

☆!farewell: 查询欢送情况
☆!whitelist: 查询安全名单
注意事项:
1.为了维护新人群环境,主群2000-2500pp,分群4400-4500pp,候补群2500-3000pp的玩家将会进入离群倒计时
2.时间由玩家当前pp决定,主群每提升3pp,分群每提升1pp,候补群每提升5pp则减少一天倒计时
3.安全名单内的成员不会受到本系统影响
4.如果进入倒计时后该玩家成为了上述人员,则时间结束后不会触发踢人,欢送名单会自动删去'''
    return txt


def ppSuggestSystem():
    txt = '''pp图推荐系统介绍

☆!getmap (with mod) (for id): 括号内为可选参数，即为指定的Mod和玩家找图(参数为mod和osuid)。如果不指定Mod，则为全mod找图；如果不指定玩家，则默认为自己找图。
☆!banmap: 为自己屏蔽某张图的推荐(参数为bid)
☆!mapinfo: 查询地图详细信息(参数为bid)
使用举例:
!getmap with hrdt for DalouBot
注意事项:
1.为每位玩家推荐pp图,使用前推荐先用!myid绑定自己
2.推荐结果是基于统计得到的，统计范围是你的pp(-150, +350)的其他玩家
3.会过滤掉你的bp前50图
4.NC会被对待成DT
5.HD、PF、SD、SO、NF会被对待成None,统计时候如果有人开了这几个Mod,会将他的pp按照None情况估算后再进行推荐
6.某图打的人越多或在他们的bp中越靠前,则推荐结果里的排名也越靠前
7.屏蔽指令实际上针对的是自己的uid,他人为您找图时候也会生效
8.私聊使用本系统会返回更为详细的结果
9.地图数据库更新日期180925'''
    return txt


def healthSystem():
    txt = '''健康系统介绍

☆!health: 加入健康套餐列表中
☆!stop_h: 将自己从健康套餐列表中移除
☆!care: 查询健康套餐名单
套餐效果:
每天凌晨0-6点时期如果在群内发言,将直接禁言至6点。
本bot是管理员的群中才会生效'''
    return txt


def mieGame():
    txt = '''1+1游戏介绍

bot算法由咩羊提供
☆!game_mie: 开始游戏,可选难度(缺省值2)
☆!stop_g: 强制结束游戏
难度说明:
1 教学级
2 高手级
3 大神级
4 噩梦级
5 退群删游戏级
游戏介绍:
你和bot各拥有两个数字,双方轮流行动,每方取出自己一个数去加对面的一个数,如果和大于10则减去10,直到某一方的两个数字均为0则获胜。游戏过程中数字0不得作为加或者被加的对象,这点请注意。
操作方法:
正确输入格式为:x y,其中x是你的其中一只手的数字,y是bot其中一只手的数字,且均取值1~9之间'''
    return txt


def watchSystem():
    txt = '''监视系统介绍

此系统开启或者关闭需要权限
☆!set_bp: 加入本群监视列表中(需要参数,第一个参数为你的用户名;第二个参数为mode,缺省值0;两个参数间用半角逗号隔开)
☆!reset_bp: 从本群监视列表中移除(参数同上)
☆!bp: 查询监视名单
使用举例:
!set_bp Aero-zero,3
监视效果:
1.当用户刷新或倒刷了bp前20,则会进行通知
2.只对500pp以上的玩家生效,监视数量上限为80
3.目前采用按群通知的方式,如果想在多个群内同时通知bp更新,则需要各个群都设置一遍(不会占用额外监视名额)'''
    return txt


def dalouCardGame():
    txt = '''DalouCard活动介绍

☆!start_card: 加入活动(参数为你的osuid)
☆!mygame: 查询活动记录
☆!mycard: 查询自己图鉴
☆!mymedal: 查询自己成就
☆!myMR: 查询抽到的某类型卡
☆!update: 更新打图记录
☆!pick: 单抽(-10金币)
☆!pick11: 11连(-100金币)
☆!pickall: 全抽(-100n金币)
☆!fly: 偷渡(-5飞机票)
☆!pt_top: 查询pt榜
☆!mn_top: 查询金币榜
☆!lucky_top: 查询欧皇榜
☆!rankme: 查询自己的排名
☆!boom: 爆炸(-30金币)
活动说明:
1.玩家可以通过打图来涨金币,金币可以用来抽卡
2.活动pt为你的仓库全部卡价值总和
3.除了注册，其余指令均可以私聊
4.第九期活动截止11月30日晚
5.卡池信息 https://yiqixie.com/s/home/fcADfeuCo_X4wGAPgehzK4A9-'''
    return txt


def chartSystem():
    txt = '''新人群chart介绍

本活动仅在新人群主群有效
☆!chart: 查询本期指定图
☆!mychart: 查询自己的成绩
☆!submit: 提交近期15次成绩
☆!chart_top: 查询每张图的榜单(可选参数,参数为指定bid,此时返回前十名结果;若不指定参数则返回本期全部chart各前三名结果)
功能还在开发中,敬请期待'''
    return txt


def suitL(list_g):
    msg = 'bot的功能仅在下列群适用\n'
    for group in list_g:
        msg = msg + '%s\n' % group
    msg = msg + '群代码从上往下依次记为1,2,3,…… (私聊解除禁言时候会用到)'
    msg = msg + '\n【注】部分指令的适用范围更小,例如!start_card只允许在新人群内使用'
    return msg


def careL(list_h):
    if not list_h:
        msg = '健康套餐名单为空'
    else:
        msg = '健康套餐名单如下(QQ号):'
        for user in list_h:
            msg = msg + '\n%s' % user
    return msg


def dogL(list_d):
    msg = '权限者列表如下(QQ号):\n'
    for user in list_d:
        msg = msg + '%s\n' % user
    msg = msg + '在一般群员基础上,权限者多拥有下列指令:\n!watch  !stop_w\n!kill@  !stop_k@\n' \
                '!smoke@  !unsmoke@\n!update  !updateall\n!ban_card  !stop_mie\n!unbind  !send'
    return msg


def killL(list_k):
    msg = '即将被踢的成员如下:\n'
    msg = msg + '群号, QQ号, 剩余时间(分)'
    for user in list_k:
        msg = msg + '\n%s, %s, %s' % (user['group'], user['qq'], user['time'])
    return msg


def eggL(list_e):
    msg = '本期已解锁彩蛋信息如下:\n编号, 关键词, 解锁者'
    for egg in list_e:
        if egg['unlock_qq']:
            if egg['unlock_name'] and egg['unlock_name'] != '0':
                msg = msg + '\n%s, %s, %s' % (egg['id'], egg['keyword'], egg['unlock_name'])
            else:
                msg = msg + '\n%s, %s, QQ号%s' % (egg['id'], egg['keyword'], egg['unlock_qq'])
    msg = msg + '\n目前彩蛋系统已经永久关闭。本期彩蛋总数: %s' % len(list_e)
    return msg


def farewellL(list_f, qq):
    list_farewell = copy.deepcopy(list_f)
    list_farewell.sort(key=lambda x: x['deadline'], reverse=False)
    member_number = min(len(list_farewell), 5)
    if not member_number:
        msg = '所有人都很安全,哈哈'
    else:
        msg = '最近有人会在指定日期离群:'
        msg2 = ''
        for i in range(len(list_farewell)):
            group = getGroupName(bot_global.group_main_list.index(list_farewell[i]['group']))
            name = list_farewell[i]['name']
            deadline = list_farewell[i]['deadline']
            if member_number:
                msg = msg + '\n%s, %s, %s' % (group, name, deadline)
                member_number = member_number - 1
            if list_farewell[i]['qq'] == qq:
                msg2 = msg2 + '\n%s, %s, %s' % (group, name, deadline)
        if not msg2:
            msg = msg + '\n------------------\n检查完毕,您没在名单中'
        else:
            msg = msg + '\n------------------\n其中,这是您的离群信息:' + msg2
    return msg


def whiteL(list_w1, list_w2):
    msg = '以下人员免除超限检测:'
    msg = msg + '\n【1】该群的群主与管理员'
    msg = msg + '\n【2】该群的其余bot'
    msg = msg + '\n【3】本bot的权限者'
    msg = msg + '\n【4】白名单玩家(QQ号):'
    for user in list_w1:
        msg = msg + '\n%s' % user
    msg = msg + '\n【5】主群参观团(QQ号):'
    for user in list_w2:
        msg = msg + '\n%s' % user
    msg = msg + '\n如果您是上述之一成员但是被检测到,请立刻联系dalou'
    return msg


def bpL(list_b, group):
    msg = ''
    std_msg = ''
    taiko_msg = ''
    ctb_msg = ''
    mania_msg = ''
    for user in list_b:
        if group not in user[20]['user_group']:
            pass
        elif user[20]['user_mode'] == '0':
            std_msg = std_msg + '%s\n' % user[20]['user_name']
        elif user[20]['user_mode'] == '1':
            taiko_msg = taiko_msg + '%s\n' % user[20]['user_name']
        elif user[20]['user_mode'] == '2':
            ctb_msg = ctb_msg + '%s\n' % user[20]['user_name']
        elif user[20]['user_mode'] == '3':
            mania_msg = mania_msg + '%s\n' % user[20]['user_name']
    if std_msg:
        msg = msg + '【std】\n%s' % std_msg
    if taiko_msg:
        msg = msg + '【taiko】\n%s' % taiko_msg
    if ctb_msg:
        msg = msg + '【ctb】\n%s' % ctb_msg
    if mania_msg:
        msg = msg + '【mania】\n%s' % mania_msg
    if not msg:
        msg = 'bot在本群内没有对任何人进行bp监视'
    else:
        msg = '本群监视列表如下:\n'+ msg + '上述成员更新bp将会进行实时通知 (用户id仅供参考,不排除有人改名,此时需要本人更新bp才会自动替换为新id)'
    return msg


def getGroupName(i):
    if i == 0:
        return '主群'
    if i == 1:
        return '分群'
    if i == 2:
        return '后花园'
    if i == 3:
        return '主群候补群'
    else:
        return '鬼知道什么群'