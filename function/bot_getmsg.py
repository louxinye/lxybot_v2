# -*- coding: utf-8 -*-
# 函数功能:查看各类帮助文档或者列表


def getHelp():
    txt = '''发烟bot使用说明

!group  查看适用群
!sorry  发超星图主动认错
!rest   1小时休息套餐
!sleep  6小时睡眠套餐
!afk    闭群套餐(可选参数)
!remove 私聊解禁
!roll   随机取数(可选参数)
!kill   查询机票获得者
!myid   绑定id
!找图系统
!健康系统
!复读系统
!监视系统
!咩羊游戏
!月常活动
!dog   查询bot权限者

v1.60 正式版'''
    return txt


def ppSuggestSystem():
    txt = '''pp图推荐系统介绍

☆!getmap (with mod) (for id): 括号内为可选参数，即为指定的Mod和玩家找图(参数为mod和osuid)。如果不指定Mod，则为全mod找图；如果不指定玩家，则默认为自己找图。
☆!banmap: 为自己屏蔽某张图的推荐(参数为bid)
☆!mapinfo: 查询地图详细信息(参数为bid)
使用举例:
!getmap with hrdt
!getmap for DalouBot
注意事项:
1.为每位玩家推荐pp图,使用前推荐先用!myid绑定自己
2.推荐结果是基于统计得到的，统计范围是你的pp(-150, +350)的其他玩家
3.会过滤掉你的bp前50图
4.NC会被对待成DT
5.HD、PF、SD、SO、NF会被对待成None,统计时候如果有人开了这几个Mod,会将他的pp按照None情况估算后再进行推荐
6.结果按照推荐指标排序,指标越大说明这图打的人越多或在他们的bp中越靠前;给出的参考pp是他们平均pp
7.屏蔽指令实际上针对的是自己的uid,他人为您找图时候也会生效'''
    return txt


def noiseSystem():
    txt = '''复读惩罚系统介绍

此系统开启或者关闭需要权限
开启后效果:
1.当同一句话被连续发送3次,bot会立刻成为第四位复读者
2.bot自动复读之后,凡是继续复读的成员立刻被禁言5分钟
3.当回复内容带有图片时,bot可能不会自动复读但是依旧计数（也就是说发第四张图片可能就会直接禁言）'''
    return txt


def healthSystem():
    txt = '''健康系统介绍

☆!health: 加入健康套餐列表中
☆!stop_h: 将自己从健康套餐列表中移除
☆!care: 查询健康套餐名单
套餐效果:
每天凌晨0-6点时期如果在群内发言,将直接禁言至6点'''
    return txt


def mieGame():
    txt = '''1+1游戏介绍

bot算法由咩羊提供
☆!game_mie: 开始游戏,可选难度(缺省值2)
☆!stop_g: 强制结束游戏
难度说明:
1 教学级
2 大神级
3 噩梦级
4 怀疑人生级
5 退群删游戏级
游戏介绍:
你和bot各拥有两个数字,双方轮流行动,每方取出自己一个数去加对面的一个数,如果和大于10则减去10,直到某一方的两个数字均为0则获胜。游戏过程中数字0不得作为加或者被加的对象,这点请注意。
操作方法:
正确输入格式为:x y,其中x是你的其中一只手的数字,y是bot其中一只手的数字,且均取值1~9之间'''
    return txt


def watchSystem():
    txt = '''监视系统介绍

此系统开启或者关闭需要权限
☆!set_bp: 加入监视列表中(需要参数, 第一个参数为你的用户名; 第二个参数为mode, 缺省值0; 两个参数间用半角逗号隔开)
☆!reset_bp: 从监视列表中移除(参数同上)
☆!bp: 查询监视名单
使用举例:
!set_bp Aero-zero,3
监视效果:
1.当用户刷新了bp前20,则会全群通知
2.当用户倒刷了一张原本为bp前20的图,则会全群通知
【提醒】只对300pp以上的玩家生效,监视数量上限为40。
'''
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
☆!rank: 查询玩家排名(参数为osuid)
☆!card: 查询玩家图鉴(参数为osuid)
☆!card_p: 查询抽卡概率
☆!card_v: 查询卡牌价值
活动说明:
1.玩家可以通过打图来涨金币,金币可以用来抽卡
2.相同卡会自动强化等级+1
3.活动pt为你的仓库全部卡价值总和
4.除了注册，其余指令均可以私聊
5.第二期活动截止3月31日晚'''
    return txt


def suitL(list_g):
    msg = 'bot的功能仅在下列群适用\n'
    for group in list_g:
        msg = msg + '%s\n' % group
    msg = msg + '群代码从上往下依次记为1,2,3,…… (私聊解除禁言时候会用到)'
    msg = msg + '\n【注】新人群主群只有月常活动和推荐pp图相关功能，别的全部失效'
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
    msg = msg + '在一般群员基础上,权限者多拥有下列指令:\n!noise  !stop_n\n!kill  !stop_k\n!watch  !stop_w\n!smoke  !unsmoke\n!ban_card'
    return msg


def bpL(list_b):
    msg = ''
    std_msg = ''
    taiko_msg = ''
    ctb_msg = ''
    mania_msg = ''
    for user in list_b:
        if user[20]['user_mode'] == '0':
            std_msg = std_msg + '%s\n' % user[20]['user_name']
        if user[20]['user_mode'] == '1':
            taiko_msg = taiko_msg + '%s\n' % user[20]['user_name']
        if user[20]['user_mode'] == '2':
            ctb_msg = ctb_msg + '%s\n' % user[20]['user_name']
        if user[20]['user_mode'] == '3':
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
        msg = 'bot没有对任何人进行bp监视'
    else:
        msg = '监视列表如下:\n'+ msg + '上述成员更新bp将会进行实时通知 (用户id仅供参考,不排除有人改名,此时需要本人更新bp才会自动替换为新id)'
    return msg
