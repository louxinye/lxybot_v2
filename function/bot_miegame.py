# -*- coding: utf-8 -*-
# 1+1游戏,算法由咩羊提供
import re
import random


# 输入当前的局面以及玩家下达的指令，计算输出新的局面、回馈消息、游戏是否结束标记
def one_plus_one_check(list_g, content, diff):
    check_input = re.match(r'^[123456789] [123456789]$', content)
    msg2 = ''
    gg = 0
    if check_input:
        user_x = int(content[0])
        user_y = int(content[2])
        if user_x != list_g[1][0] and user_x != list_g[1][1]:
            msg1 = '输入错误,你需要使用自己的其中一只手的数字而不是%s\nbot目前数字: %s %s\n玩家目前数字: %s %s' % (user_x,
                    list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
        elif user_y != list_g[0][0] and user_y != list_g[0][1]:
            msg1 = '输入错误,你需要指定bot的其中一只手的数字而不是%s\nbot目前数字: %s %s\n玩家目前数字: %s %s' % (user_y,
                    list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
        else:
            for i in range(0, 2):
                if user_x == list_g[1][i]:
                    for j in range(0, 2):
                        if user_y == list_g[0][j]:
                            list_g[1][i] = (list_g[1][i] + user_y) % 10
                            break
                    break
            msg1 = '操作成功!\nbot目前数字: %s %s\n玩家目前数字: %s %s' % (list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
            did = ai(list_g, 0, 0, diff)
            if list_g[0][did // 2] == 0 or list_g[1][did % 2] == 0:
                msg2 = '咩羊发现自己算错了,他放弃了!'
                gg = 1
            else:
                msg2 = 'bot经过一番计算，决定使用它的数字%s碰你的数字%s\n' % (list_g[0][did // 2], list_g[1][did % 2])
                list_g[0][did // 2] = (list_g[0][did // 2] + list_g[1][did % 2]) % 10
                msg2 = msg2 + 'bot目前数字: %s %s\n玩家目前数字: %s %s' % (list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
            if list_g[0][0] == 0 and list_g[0][1] == 0:
                msg2 = msg2 + '\nbot胜利!'
                gg = 1
            elif list_g[1][0] == 0 and list_g[1][1] == 0:
                msg2 = msg2 + '\n玩家胜利!'
                gg = 1
    else:
        msg1 = '输入错误!\n正确输入格式为:x y\n其中x是你的其中一只手的数字,y是bot其中一只手的数字,且均取值1~9之间\n' \
               'bot目前数字: %s %s\n玩家目前数字: %s %s' % (list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
    return msg1, msg2, gg


def ai(finger, lvl, zero, diff):
    level = lvl
    level = level + 1
    if level == 1:
        for i in range(0, 2):
            for j in range(0, 2):
                if finger[i][j] == 0:
                    zero = zero + 1
    zero_ = 0  # 每次都判断的0的数量
    for i in range(0, 2):
        for j in range(0, 2):
            if finger[i][j] == 0:
                zero_ = zero_ + 1
    if zero_ == 2 and lvl:  # 最终结局计算
        fig1 = finger[0][0] + finger[0][1]
        fig2 = finger[1][0] + finger[1][1]
        score = ender(fig1, fig2)
        if level % 2 == 0:
            if score == 0:
                score = 90
            return score
        else:
            if score == 0:
                score = -90
            return score
    score_list = [[-200, -200], [-200, -200]]  # 0左1右，AI在前
    if zero == 1:
        level_max = diff * 2
    else:
        level_max = diff
    if level < level_max:
        if finger[0][0] == finger[0][1]:
            i_max = 1
        else:
            i_max = 2
        if finger[1][0] == finger[1][1]:
            j_max = 1
        else:
            j_max = 2
        for i in range(0, i_max):
            if finger[0][i]:
                for j in range(0, j_max):
                    if finger[1][j]:
                        ai_new = [[finger[0][0], finger[0][1]], [finger[1][0], finger[1][1]]]
                        ai_new[0][i] = (ai_new[0][i] + finger[1][j]) % 10
                        score_list[i][j] = estimation(ai_new, level)
                        if score_list[i][j] == 100:
                            if level > 1:
                                return 100
                            else:
                                return 2 * i + j
                        else:
                            for k in range(0, 2):
                                temp = ai_new[0][k]
                                ai_new[0][k] = ai_new[1][k]
                                ai_new[1][k] = temp
                            score_list[i][j] = -ai(ai_new, level, zero, diff)
                            if score_list[i][j] == 100:
                                if level > 1:
                                    return 100
                                else:
                                    return 2 * i + j
    else:
        return estimation(finger)
    trap = 0  # 陷阱加分
    if lvl % 2 == 1:
        for i in range(0, 2):
            for j in range(0, 2):
                if finger[0][i] * finger[1][j] > 0 and finger[0][i] + finger[1][j] == 10:
                    trap = trap - 1
    max_score = score_list[0][0]
    for i in range(0, 2):
        for j in range(0, 2):
            if score_list[i][j] > max_score:
                max_score = score_list[i][j]
    if level > 1:
        return max_score + trap
    able = [[0, 0], [0, 0]]
    for i in range(0, 2):
        for j in range(0, 2):
            if score_list[i][j] == max_score:
                able[i][j] = 1
    things_can_be_done = 0
    for i in range(0, 2):
        for j in range(0, 2):
            things_can_be_done = things_can_be_done + able[i][j]
    will_do = yran(things_can_be_done)
    for i in range(0, 2):
        for j in range(0, 2):
            if able[i][j]:
                if will_do == 0:
                    return 2 * i + j
                else:
                    will_do = will_do - 1


def estimation(fig, level=0):
    a = 0
    b = 0
    if level != 0:
        if level % 2 == 1:
            a = 1
        else:
            b = 1
    score = 0
    for i in range(0, 2):
        if fig[0][i] == 0:
            score = score + 30 + b * 5
        if fig[1][i] == 0:
            score = score - 30 - a * 5
    if fig[0][0] == fig[0][1]:
        score = score - 10
    if fig[1][0] == fig[1][1]:
        score = score + 10
    if fig[0][0] == 0 and fig[0][1] == 0:
        score = 100
    if fig[1][0] == 0 and fig[1][1] == 0:
        score = -100
    if (fig[0][0] + fig[0][1] + fig[1][0] + fig[1][1]) == 0:
        score = 0
    return score


def ender(figin1, figin2):
    fig = [figin1, figin2]
    for i in range(0, 3):
        if fig[0] != 0 and fig[1] != 0:
            fig[0] = (fig[0] + fig[1]) % 10
            fig[1] = (fig[1] + fig[0]) % 10
    draw = [fig[0], fig[1]]
    while fig[0] and fig[1]:
        fig[0] = (fig[0] + fig[1]) % 10
        fig[1] = (fig[1] + fig[0]) % 10
        if draw[0] == fig[0] and draw[1] == fig[1]:
            break
    if fig[0] == 0:
        return 100
    elif fig[1] == 0:
        return -100
    else:
        return 0


def yran(a):
    return random.randint(0, a-1)


# 函数功能:!game指令检查
def startGame(game_content, game_member, member_qq, content):
    if content == '!game_mie':
        if game_member:
            level_max = 0
            msg = '该游戏正在被玩家%s占用,若要停止则需要本人使用!stop_g' % game_member
        else:
            level_max = 4
            game_member = member_qq
            game_content = [[1, 1], [1, 1]]
            msg = '锁定玩家成功!\n难度: 大神级\nbot目前数字:1 1\n玩家目前数字:1 1'
    elif '!game_mie ' in content:
        if game_member:
            level_max = 0
            msg = '该游戏正在被玩家%s占用,若要停止则需要本人使用!stop_g' % game_member
        else:
            (level_max, name) = game_diff(content)
            if level_max > 0:
                game_member = member_qq
                game_content = [[1, 1], [1, 1]]
                msg = '锁定玩家成功!\n难度: %s\nbot目前数字:1 1\n玩家目前数字:1 1' % name
            else:
                msg = '难度输入有误'
    else:
        level_max = 0
        msg = '无法识别,bot猜测您是想使用指令!game x (x为参数,缺省值2)'
    return game_content, game_member, msg, level_max


def game_diff(content):
    check_game = re.match(r'^!game_mie [12345]$', content)
    if check_game:
        t = int(content[10])
        if t == 1:
            level_max = 2
            diff_name = '教学级'
        elif t == 2:
            level_max = 3
            diff_name = '大神级'
        elif t == 3:
            level_max = 4
            diff_name = '噩梦级'
        elif t == 4:
            level_max = 6
            diff_name = '怀疑人生级'
        elif t == 5:
            level_max = 8
            diff_name = '退群删游戏级'
        else:
            level_max = 0
            diff_name = '???级'
    else:
        level_max = 0
        diff_name = '???级'
    return level_max, diff_name
