# -*- coding: utf-8 -*-
import xlwt
from function import bot_IOfile


def outputExcel():
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1',cell_overwrite_ok=True)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = u'宋体'
    font.height = 240
    style.font = font
    user_card_list = bot_IOfile.read_pkl_data('D:\Python POJ\lxybot_v2\data\data_card_game_list.pkl')
    sheet.col(0).width = 256*15
    sheet.col(1).width = 256*20
    sheet.col(2).width = 256*9
    sheet.col(3).width = 256*9
    sheet.col(4).width = 256*9
    sheet.col(5).width = 256*9
    sheet.col(6).width = 256*9
    sheet.col(7).width = 256*9
    sheet.col(8).width = 256*9
    sheet.col(9).width = 256*9
    sheet.col(10).width = 256*12
    sheet.col(11).width = 256*12
    sheet.col(12).width = 256*12
    sheet.col(13).width = 256*12
    sheet.col(14).width = 256*12
    sheet.write(0, 0, 'qq号', style)
    sheet.write(0, 1, 'osuid', style)
    sheet.write(0, 2, '总金币', style)
    sheet.write(0, 3, '总积分', style)
    sheet.write(0, 4, '爆炸费', style)
    sheet.write(0, 5, 'MR总数', style)
    sheet.write(0, 6, 'UR总数', style)
    sheet.write(0, 7, 'SR总数', style)
    sheet.write(0, 8, 'R总数', style)
    sheet.write(0, 9, 'N总数', style)
    sheet.write(0, 10, '水王之王', style)  # 统计抽到whir卡的数量
    sheet.write(0, 11, '欧皇系数', style)
    sheet.write(0, 12, '金币排名', style)
    sheet.write(0, 13, '积分排名', style)
    sheet.write(0, 14, '欧洲排名', style)
    for i in range(len(user_card_list)):
        sheet.write(i+1, 0, '%s' % user_card_list[i]['qq'], style)
        sheet.write(i+1, 1, user_card_list[i]['name'], style)
        sheet.write(i+1, 2, user_card_list[i]['total_money'], style)
        sheet.write(i+1, 3, user_card_list[i]['pt'], style)
        sheet.write(i+1, 4, user_card_list[i]['boom_money'], style)
        sheet.write(i+1, 5, eachCardNum(user_card_list[i]['card'], 0), style)
        sheet.write(i+1, 6, eachCardNum(user_card_list[i]['card'], 1), style)
        sheet.write(i+1, 7, eachCardNum(user_card_list[i]['card'], 2), style)
        sheet.write(i+1, 8, eachCardNum(user_card_list[i]['card'], 3), style)
        sheet.write(i+1, 9, eachCardNum(user_card_list[i]['card'], 4), style)
        sheet.write(i+1, 10, certainCardNum(user_card_list[i]['card'][4], 'whirLeeve'), style)  # 如果没有此成就请删掉这行即可
        if totalCardNum(user_card_list[i]['card']) > 0:
            sheet.write(i+1, 11, '%.3f' % user_card_list[i]['lucky_rate'], style)
        else:
            sheet.write(i+1, 11, 0, style)
    wbk.save('D:\Python POJ\lxybot_v2\offline\output.xls')


def totalCardNum(card_set):
    num = 0
    for i in range(5):
        for card in card_set[i]:
            num = num + card['card_number']
    return num


def eachCardNum(card_set, i):
    num = 0
    for card in card_set[i]:
        num = num + card['card_number']
    return num


def certainCardNum(card_rare_set, name):
    for card in card_rare_set:
        if card['card_name'] == name:
            return card['card_number']
    return 0

outputExcel()