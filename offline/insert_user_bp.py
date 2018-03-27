# -*- coding: UTF-8 -*-
# 按照list顺序依次查询用户bp并加入数据库
from function import bot_osu
from function import bot_IOfile
from function import bot_SQL


def get_mod(mod_id, pp):
    mod = int(mod_id)
    total_mod = mod
    mod_list = ['NF', 'EZ', '', 'HD', 'HR', 'SD', 'DT', 'RL', 'HT', 'NC', 'FL', 'AT', 'SO', 'AP', 'PF',
                '4K', '5K', '6K', '7K', '8K', 'FI', 'RD', 'LM', '', '9K', '10K', '1K', '2K', '3K']
    choose = []
    for i in range(28, -1, -1):
        if mod >= 2**i:
            choose.append(mod_list[i])
            mod = mod - 2**i
            if mod_list[i] == 'NC':
                mod = mod - 64
            if mod_list[i] == 'PF':
                mod = mod - 32
    # 优化mod
    for i in range(len(choose)):
        if choose[i] == 'NC':  # NC改成DT
            total_mod = total_mod - 512
        if choose[i] == 'PF':  # PF删除
            total_mod = total_mod - 16384 - 32
        if choose[i] == 'SD':  # SD删除
            total_mod = total_mod - 32
        if choose[i] == 'SO':  # SO删除，得分乘以1.05
            total_mod = total_mod - 4096
            pp = int(pp * 1.05)
        if choose[i] == 'NF':  # NF删除，得分乘以1.09
            total_mod = total_mod - 1
            pp = int(pp * 1.09)
        if choose[i] == 'HD':  # HD删除，得分除以1.10
            total_mod = total_mod - 8
            pp = int(pp / 1.1)
    return total_mod, pp


error_list = []
user_list = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_cn_list.pkl')
print(len(user_list))
user_number = 0
for user in user_list:
    user_number = user_number + 1
    uid = user['uid']
    user_pp = user['pp']
    result = bot_osu.getUserBp(uid, 0)
    if not result:
        error_list.append(user)
        print('%s. %s的成绩获取失败' % (user_number, uid))
    elif len(result) < 30:
        print('%s. %s的bp数少于30个' % (user_number, uid))
    else:
        bp_rank = 0
        for bp_msg in result:
            bp_rank = bp_rank + 1
            if bp_rank > 30:
                break
            bid = int(bp_msg['beatmap_id'])
            mod = int(bp_msg['enabled_mods'])
            score_pp = int(float(bp_msg['pp']))
            (new_mod, new_pp) = get_mod(mod, score_pp)
            sql = 'INSERT INTO bp_mode0_msg VALUES (%d, %d, %d, %d, %d, %d, %d, %d)' % (uid, bp_rank, bid, mod, score_pp, user_pp, new_mod, new_pp)
            bot_SQL.action(sql)
        print('%s. %s的bp记录完毕' % (user_number, uid))
bot_IOfile.write_pkl_data(error_list, 'D:\Python POJ\lxybot_v2\data\data_error_cn_list.pkl')


