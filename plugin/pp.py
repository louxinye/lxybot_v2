import math
from plugin.map_types import Mods


def base_strain(strain):
    return math.pow(5.0 * max(1.0, strain / 0.0675) - 4.0, 3.0) / 100000.0


def acc_calc(c300, c100, c50, misses):
    total_hits = c300 + c100 + c50 + misses
    acc = 0.0
    if total_hits > 0:
        acc = (c50 * 50.0 + c100 * 100.0 + c300 * 300.0) / (total_hits * 300.0)
    return acc


class PPCalcResult:
    def __init__(self):
        self.acc_percent = 0
        self.pp = 0
        self.aim_pp = 0
        self.speed_pp = 0
        self.acc_pp = 0


def calculate_pp(aim, speed, btmap, c100, c50, misses, used_mods=Mods(), combo=None, score_version=1, c300=None):
    res = PPCalcResult()
    od = btmap.od
    ar = btmap.ar
    circles = btmap.num_circles

    if c100 > btmap.num_objects or c50 > btmap.num_objects or misses > btmap.num_objects:
        print("Invalid accuracy number")
        return res

    if c300 is None:
        c300 = btmap.num_objects - c100 - c50 - misses

    if not combo:
        combo = btmap.max_combo
    elif combo == 0:
        print("Invalid combo count")
        return res

    total_hits = c300 + c100 + c50 + misses
    if total_hits != btmap.num_objects:
        print("warning hits != objects")

    if score_version != 1 and score_version != 2:
        print("Score version not found")
        return res

    acc = acc_calc(c300, c100, c50, misses)
    res.acc_percent = acc * 100.0

    aim_value = base_strain(aim)

    total_hits_over_2k = total_hits / 2000.0
    length_bonus = 0.95 + 0.4 * min(1.0, total_hits_over_2k) + (
        math.log10(total_hits_over_2k) * 0.5 if total_hits > 2000 else 0.0)

    miss_penalty = math.pow(0.97, misses)

    combo_break = math.pow(combo, 0.8) / math.pow(btmap.max_combo, 0.8)

    aim_value *= length_bonus
    aim_value *= miss_penalty
    aim_value *= combo_break

    ar_bonus = 1.0

    if ar > 10.33:
        ar_bonus += 0.45 * (ar - 10.33)
    elif ar < 8:
        low_ar_bonus = 0.01 * (8 - ar)

        if used_mods.hd:
            low_ar_bonus *= 2.0

        ar_bonus += low_ar_bonus

    aim_value *= ar_bonus

    if used_mods.hd:
        aim_value *= 1.18

    if used_mods.fl:
        aim_value *= 1.45 * length_bonus

    acc_bonus = 0.5 + acc / 2.0

    od_bonus = 0.98 + math.pow(od, 2) / 2500.0

    aim_value *= acc_bonus * od_bonus
    res.aim_pp = aim_value

    speed_value = base_strain(speed)
    speed_value *= length_bonus * miss_penalty * combo_break * acc_bonus * od_bonus
    res.speed_pp = speed_value

    real_acc = 0.0

    if score_version == 2:
        circles = total_hits
        real_acc = acc
    else:
        if circles:
            real_acc = ((c300 - (total_hits - circles)) * 300 + c100 * 100 + c50 * 50) / (circles * 300)
        real_acc = max(0.0, real_acc)

    acc_value = math.pow(1.52163, od) * real_acc ** 24.0 * 2.83

    acc_value *= min(1.15, (circles / 1000.0) ** 0.3)

    if used_mods.hd:
        acc_value *= 1.02
    if used_mods.fl:
        acc_value *= 1.02

    res.acc_pp = acc_value

    final_multiplier = 1.12
    if used_mods.nf:
        final_multiplier *= 0.90
    if used_mods.so:
        final_multiplier *= 0.95
    res.pp = (aim_value ** 1.1 + speed_value ** 1.1 + acc_value ** 1.1) ** (1.0 / 1.1) * final_multiplier
    return res


def calculate_pp_by_acc(aim, speed, b, acc_percent, used_mods=Mods(), combo=65535, misses=0, score_version=1):
    misses = min(b.num_objects, misses)

    max300 = (b.num_objects - misses)

    acc_percent = max(0.0, min(acc_calc(max300, 0, 0, misses) * 100.0, acc_percent))

    c50 = 0

    c100 = round(-3.0 * ((acc_percent * 0.01 - 1.0) * b.num_objects + misses) * 0.5)

    if c100 > b.num_objects - misses:
        c100 = 0
        c50 = round(-6.0 * ((acc_percent * 0.01 - 1.0) * b.num_objects + misses) * 0.2)

        c50 = min(max300, c50)
    else:
        c100 = min(max300, c100)

    c300 = b.num_objects - c100 - c50 - misses

    return calculate_pp(aim, speed, b, misses, c100, c50, used_mods, combo, score_version, c300)
