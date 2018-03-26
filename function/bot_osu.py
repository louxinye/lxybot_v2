# -*- coding: utf-8 -*-
# osu相关系统
import requests
import json
import re
from function import bot_IOfile
from function import bot_SQL


osu_api_key = '7f2f84a280917690158a6ea1f7a72b7e8374fbf9'
headers = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language' : 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
}
bp_list = []


def set_id(list_b, content):
    if len(list_b) > 39:
        msg = '达到40人上限!'
    elif content == '!set_bp':
        msg = '倒是告诉我id啊'
    elif '!set_bp ' in content:
        check_id = re.match(r'^!set_bp (.*),([0123])$', content)
        if check_id:
            osu_name = check_id.group(1)
            osu_mode = check_id.group(2)
            print('1 %s' % osu_mode)
        else:
            check_id = re.match(r'^!set_bp (.*)$', content)
            if check_id:
                osu_name = check_id.group(1)
                osu_mode = '0'
                print('2 %s' % osu_mode)
            else:
                msg = '您的!set_bp指令使用错误'
                return msg
        (osu_id, real_name, pp, pc, tth, acc) = get_info(osu_name, osu_mode)
        if not osu_id:
            msg = '查不到这个人哎'
        elif pp < 300:
            msg = '该号pp较低, 不进行监视'
        else:
            success = 1
            for user in list_b:
                if user[20]['user_id'] == osu_id and user[20]['user_mode'] == osu_mode:
                    success = 0
                    break
            if success == 1:
                bp_msg = get_bp(osu_id, osu_mode)
                if len(bp_msg) > 19:
                    new_bp_msg = []
                    for i in range(20):
                        new_bp_msg.append(bp_msg[i])
                    user_msg = {'user_id': osu_id, 'user_name': real_name, 'user_mode': osu_mode}
                    new_bp_msg.append(user_msg)
                    list_b.append(new_bp_msg)
                    msg = '添加bp监视成功!'
                    bot_IOfile.write_pkl_data(list_b, 'D:\Python POJ\lxybot\data\data_bp_care_list.pkl')
                else:
                    msg = 'bp数量低于20个,不进行监视'
            else:
                msg = '已经存在此id,无需重复添加'
    else:
        msg = '无法识别,bot猜测您是想使用指令!set_bp x(x为参数)'
    return msg


def stop_set_id(list_b, content):
    if content == '!reset_bp':
        msg = '倒是告诉我id啊'
    elif '!reset_bp ' in content:
        check_id = re.match(r'^!reset_bp (.*),([0123])$', content)
        if check_id:
            osu_name = check_id.group(1)
            osu_mode = check_id.group(2)
        else:
            check_id = re.match(r'^!reset_bp (.*)$', content)
            if check_id:
                osu_name = check_id.group(1)
                osu_mode = '0'
            else:
                msg = '您的!reset_bp指令使用错误'
                return msg
        (osu_id, real_name, pp, pc, tth, acc) = get_info(osu_name, osu_mode)
        if not osu_id:
            msg = '查不到这个人哎'
        else:
            success = 0
            bp_num = len(list_b)
            for i in range(0, bp_num):
                if list_b[i][20]['user_id'] == osu_id and list_b[i][20]['user_mode'] == osu_mode:
                    success = 1
                    del list_b[i]
                    break
            if success == 1:
                msg = '移除bp监视成功!'
                bot_IOfile.write_pkl_data(list_b, 'D:\Python POJ\lxybot\data\data_bp_care_list.pkl')
            else:
                msg = '此人并没在监视列表中'
    else:
        msg = '无法识别,bot猜测您是想使用指令!reset_bp x(x为参数)'
    return msg


# 输入用户名或uid(此时需要指明type_mode为id)，输出确切的用户信息
def get_info(osu_name, osu_mode, type_mode='string'):
    url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s&type=%s&m=%s&limit=1' % (osu_api_key, osu_name, type_mode, osu_mode)
    res = get_url(url)
    if not res:
        return 0, 0, 0, 0, 0, 0
    result = json.loads(res.text)
    if len(result) == 0:
        return 0, 0, 0, 0, 0, 0
    else:
        uid = result[0]['user_id']
        name = result[0]['username']
        pp = float(valueChange(result[0]['pp_raw']))
        pc = int(valueChange(result[0]['playcount']))
        tth = int(valueChange(result[0]['count300'])) + int(valueChange(result[0]['count100'])) + int(valueChange(result[0]['count50']))
        acc = float(valueChange(result[0]['accuracy']))
        return uid, name, pp, pc, tth, acc


# 输入uid，输出bp前50
def get_bp(osu_id, osu_mode):
    url = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s&type=id&m=%s&limit=50' % (osu_api_key, osu_id, osu_mode)
    res = get_url(url)
    if not res:
        return 0
    result = json.loads(res.text)
    if len(result) == 0:
        return 0
    else:
        return result


# 输入bid，输出图的名字难度和长度(此时需要指明getlength为True)
def get_map(bid, mode, getlength=False):
    url = 'https://osu.ppy.sh/api/get_beatmaps?k=%s&b=%s&m=%s&limit=1' % (osu_api_key, bid, mode)
    res = get_url(url)
    if not res:
        return 0
    result = json.loads(res.text)
    if len(result) == 0:
        msg = '不存在这张图'
    else:
        msg = '%s - %s [%s]\n难度: %.2f (未计算mod)'\
            % (result[0]['artist'], result[0]['title'], result[0]['version'], float(result[0]['difficultyrating']))
        if getlength:
            length = getLength(int(result[0]['total_length']))
            msg = msg + '\n长度: %s' % length
    return msg


# 输入uid，bid，输出此人打这图的pp
def get_map_pp(uid, bid, mode):
    url = 'https://osu.ppy.sh/api/get_scores?k=%s&b=%s&u=%s&type=id&m=%s&limit=1' % (osu_api_key, bid, uid, mode)
    res = get_url(url)
    if not res:
        return 0
    result = json.loads(res.text)
    if len(result) == 0:
        return 0
    else:
        pp = result[0]['pp']
        return pp


# request请求
def get_url(url):
    try:
        res = requests.get(url=url, headers=headers, params=None, timeout=3)
        return res
    except requests.exceptions.RequestException:
        return 0


# 评分转化
def get_rank(content):
    if content == 'X' or content == 'XH':
        msg = 'SS'
    elif content == 'SH':
        msg = 'S'
    else:
        msg = content
    return msg


# acc计算
def get_acc(num_33, num_22, num_11, num_00):
    num_300 = int(num_33)
    num_100 = int(num_22)
    num_50 = int(num_11)
    num_0 = int(num_00)
    total = 6 * (num_300 + num_100 + num_50 + num_0)
    real = 6 * num_300 + 2 * num_100 + num_50
    if total > 0:
        acc = real / total
        msg = '%.2f' % (acc * 100)
    else:
        msg = '???'
    return msg


# mod计算
def get_mod(mod_id):
    mod = int(mod_id)
    mod_list = ['NF', 'EZ', '', 'HD', 'HR', 'SD', 'DT', 'RL', 'HT', 'NC', 'FL', 'AT', 'SO', 'AP', 'PF',
                '4K', '5K', '6K', '7K', '8K', 'FI', 'RD', 'LM', '', '9K', '10K', '1K', '2K', '3K']
    choose = []
    msg = ''
    for i in range(28, -1, -1):
        if mod >= 2**i:
            choose.append(mod_list[i])
            mod = mod - 2**i
            if mod_list[i] == 'NC':
                mod = mod - 64
            if mod_list[i] == 'PF':
                mod = mod - 32
    num = len(choose)
    for i in range(num-1, -1, -1):
        msg = msg + '%s' % choose[i]
    if not msg:
        msg = 'None'
    return msg


# 将秒转化为时分秒结构
def getLength(len):
    if len < 1:
        msg = '算不出来'
    else:
        if len > 3599:
            hour = len // 3600
            rest = len % 3600
            minute = rest // 60
            rest = rest % 60
            msg = '%s小时%s分%s秒' % (hour, minute, rest)
        elif len > 59:
            minute = len // 60
            rest = len % 60
            msg = '%s分%s秒' % (minute, rest)
        else:
            msg = '%s秒' % len
    return msg


# 打印mode
def get_mode(mode_id):
    if mode_id == '0':
        msg = 'std'
    elif mode_id == '1':
        msg = 'taiko'
    elif mode_id == '2':
        msg = 'ctb'
    elif mode_id == '3':
        msg = 'mania'
    else:
        msg = 'unknown mode'
    return msg


# 将null转化为字符0
def valueChange(a):
    if not a:
        return '0'
    else:
        return a


# 绑定信息到数据库(目前仅用于pp图推荐)
def setid_sql(user_qq, content):
    sql = 'SELECT * FROM user WHERE qq = \'%s\' AND mode = 0' % user_qq
    result = bot_SQL.select(sql)
    if result:
        name = result[0][2]
        msg = '您已经绑定%s, 若发生错误请联系dalou' % name
        return msg
    if content == '!myid':
        msg = '倒是告诉我id啊'
    elif '!myid ' in content:
        check_id = re.match(r'^!myid (.*)$', content)
        if check_id:
            name = check_id.group(1)
            (uid, name, pp, pc, tth, acc) = get_info(name, '0')
            if not uid:
                msg = 'pp查询出错,请稍后再试'
                return msg
            sql = 'INSERT INTO user VALUES (%s, %d, \'%s\', %d, %d, %d, %.2f, 0)' % (user_qq, int(uid), name, int(pp), pc, tth, acc)
            success = bot_SQL.action(sql)
            if success:
                msg = '玩家信息:\nuid: %s\nname:%s\npp: %s\n绑定成功!' % (uid, name, pp)
            else:
                msg = '数据库出错，请联系Dalou!'
        else:
            msg = '您的!myid指令使用错误'
    else:
        msg = '无法识别,bot猜测您是想使用指令!myid x (x为参数)'
    return msg
