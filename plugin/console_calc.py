import requests

from plugin.beatmap import Beatmap
from plugin.pp import calculate_pp, Mods, calculate_pp_by_acc
from plugin import diff

def gogogo(bid, file_pass="", acc="", c300=0, c100=0, c50=0, c0=0, maxcombo_now=0, mod_name="", link=True, score_ver=1, rank='F'):
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File or url. If url provided use -link flag', )
    parser.add_argument('-link', help='Flag if url provided', action='store_true')
    parser.add_argument('-acc', help='Accuracy percentage', metavar="acc%",
                        default=0, type=float)
    parser.add_argument('-c100', help='Number of 100s',
                        metavar="100s", default=0, type=int)
    parser.add_argument('-c50', help='Number of 50s', metavar="50s",
                        default=0, type=int)
    parser.add_argument('-m', help='Number of misses', metavar="miss",
                        default=0, dest='misses', type=int)
    parser.add_argument('-c', help='Max combo', metavar="combo", default=0,
                        dest='combo', type=int)
    parser.add_argument('-sv', help='Score version 1 or 2', metavar="sv",
                        dest='score_ver', default=1, type=int)
    parser.add_argument('-mods', help='Mod string eg. HDDT', metavar="mods", default="")
    parser.add_argument('-completion', help='This gives you percentage of completion for failed plays', metavar='complete', type=int, default=0)

    args = parser.parse_args()
    c100 = args.c100
    c50 = args.c50
    misses = args.misses
    combo = args.combo
    acc = args.acc
    score_ver = args.score_ver
    mod_s = args.mods
    web_beatmap = args.link
    file_name = args.file
    complete = args.completion
    '''

    pp = [[0,0,0], [0,0,0], [0,0,0]]  # 在当前combo、多连一半的combo、fc的情况下，当前acc、多打一半acc、ss的成绩
    if link:
        data = requests.get("https://osu.ppy.sh/osu/{}".format(bid)).content.decode('utf8')
        print(data)
    else:
        data = open(file_pass, 'r').read()
    btmap = Beatmap(data)
    good = btmap.parse()
    if not good:
        raise ValueError("Beatmap verify failed. "
                         "Either beatmap is not for osu! standart, or it's malformed")
    if not maxcombo_now or maxcombo_now > btmap.max_combo:
        maxcombo_now = btmap.max_combo
    mods = Mods(mod_name if mod_name != "None" else "")
    btmap.apply_mods(mods)
    aim, speed, stars, btmap = diff.main(btmap)
    maxcombo_full = btmap.max_combo
    maxcombo_half = maxcombo_full - int((maxcombo_full - maxcombo_now) / 2)
    msg = '--------------------\n'
    msg = msg + 'stars: %.2f | %s | %s\n%sx/%sx | %s%% | %smiss\n' % \
                (stars, mod_name, rank, maxcombo_now, maxcombo_full, acc, c0)

    # 计算完成度
    complete = c300 + c100 + c50 + c0
    if complete == btmap.num_objects:
        complete = 0
    if not complete == 0:
        hitobj = []
        numobj = complete
        num = len(btmap.hit_objects)
        if numobj > num:
            numobj = num
        for objects in btmap.hit_objects:
            hitobj.append(objects.time)
        timing = int(hitobj[num - 1]) - int(hitobj[0])
        point = int(hitobj[numobj - 1]) - int(hitobj[0])
        completion = point / timing
    else:
        completion = 100

    if rank != 'F':
        pp[0][0] = calculate_pp(aim, speed, btmap, c100, c50, c0, c300=c300, used_mods=mods, combo=maxcombo_now, score_version=score_ver).pp
        pp[1][0] = calculate_pp(aim, speed, btmap, c100, c50, c0, c300=c300, used_mods=mods, combo=maxcombo_half, score_version=score_ver).pp
        pp[2][0] = calculate_pp(aim, speed, btmap, c100, c50, 0, c300=c300+c0, used_mods=mods, combo=maxcombo_full, score_version=score_ver).pp
        c100_cut = int(c100/2)
        c50_cut = int(c50/2)
        c300 = c300 + c100_cut + c50_cut
        c100 = c100 - c100_cut
        c50 = c50 - c50_cut
        pp[0][1] = calculate_pp(aim, speed, btmap, c100, c50, c0, c300=c300, used_mods=mods, combo=maxcombo_now, score_version=score_ver).pp
        pp[1][1] = calculate_pp(aim, speed, btmap, c100, c50, c0, c300=c300, used_mods=mods, combo=maxcombo_half, score_version=score_ver).pp
        pp[2][1] = calculate_pp(aim, speed, btmap, c100, c50, 0, c300=c300+c0, used_mods=mods, combo=maxcombo_full, score_version=score_ver).pp
        c300 = c300 + c100 + c50 + c0
        pp[2][2] = calculate_pp(aim, speed, btmap, 0, 0, 0, c300=c300, used_mods=mods, combo=maxcombo_full, score_version=score_ver).pp
        msg = msg + 'pp: %.1f → %.1f\n' % (pp[0][0], pp[2][2])
        if rank == 'X' or rank == 'XH':
            msg = msg + '恭喜! 你已经打爆这首歌了'
        else:
            msg = msg + '详细表(横轴acc,纵轴连击):\n%.1f  %.1f  ---\n%.1f  %.1f  ---\n%.1f  %.1f  %.1f' % \
                        (pp[0][0], pp[0][1], pp[1][0], pp[1][1], pp[2][0], pp[2][1],pp[2][2])
    else:
        accuracy = float(acc)
        pp[0][0] = calculate_pp_by_acc(aim, speed, btmap, accuracy, used_mods=mods, combo=maxcombo_now, misses=c0, score_version=score_ver).pp
        pp[1][0] = calculate_pp_by_acc(aim, speed, btmap, accuracy, used_mods=mods, combo=maxcombo_half, misses=c0, score_version=score_ver).pp
        pp[2][0] = calculate_pp_by_acc(aim, speed, btmap, accuracy, used_mods=mods, combo=maxcombo_full, misses=0, score_version=score_ver).pp
        accuracy = 100 - (100 - accuracy)/2
        pp[0][1] = calculate_pp_by_acc(aim, speed, btmap, accuracy, used_mods=mods, combo=maxcombo_now, misses=c0, score_version=score_ver).pp
        pp[1][1] = calculate_pp_by_acc(aim, speed, btmap, accuracy, used_mods=mods, combo=maxcombo_half, misses=c0, score_version=score_ver).pp
        pp[2][1] = calculate_pp_by_acc(aim, speed, btmap, accuracy, used_mods=mods, combo=maxcombo_full, misses=0, score_version=score_ver).pp
        accuracy = 100
        pp[2][2] = calculate_pp_by_acc(aim, speed, btmap, accuracy, used_mods=mods, combo=maxcombo_full, misses=0, score_version=score_ver).pp
        msg = msg + '你只完成歌曲时长的%.1f%%\n' % (completion*100)
        msg = msg + '详细表(横轴acc,纵轴连击):\n%.1f  %.1f  ---\n%.1f  %.1f  ---\n%.1f  %.1f  %.1f' % \
                    (pp[0][0], pp[0][1], pp[1][0], pp[1][1], pp[2][0], pp[2][1], pp[2][2])
    return msg

'''
    pippy_output = {
        "map": btmap.title,
        "artist": btmap.artist,
        "title": btmap.title,
        "creator": btmap.creator,
        "mods_str": mod_name,
        "ar": btmap.ar,
        "od": btmap.od,
        "hp": btmap.hp,
        "cs": btmap.cs,
        "num_circles": btmap.num_circles,
        "num_sliders": btmap.num_sliders,
        "num_spinners": btmap.num_spinners,
        "num_objects": btmap.num_objects,
        "stars": round(stars, 2),
        "acc": round(pp.acc_percent, 2),
        "combo": maxcombo_now,
        "max_combo": btmap.max_combo,
        "misses": c0,
        "pp": float("{:.2f}".format(pp)),
        "map_completion": float("{:.2f}".format(completion))
    }
'''

