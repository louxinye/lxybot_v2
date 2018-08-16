import math

from plugin.beatmap import Beatmap, HitObject

decay_base = [0.3, 0.15]

almost_diameter = 90

stream_spacing = 110
single_spacing = 125

weight_scaling = [1400, 26.25]

circlesize_buff_threshhold = 30

star_scaling_factor = 0.0675
extreme_scaling_factor = 0.5


class DiffObj:
    __slots__ = ('ho', 'strains', 'norm_start', 'norm_end', 'scaling_factor')
    
    def __init__(self, base_object: HitObject, radius: int, prev):
        radius = float(radius)
        self.ho = base_object
        self.strains = [1, 1]
        self.norm_start = 0
        self.norm_end = 0
        self.scaling_factor = 52.0 / radius
        if radius < circlesize_buff_threshhold:
            self.scaling_factor *= 1 + min((circlesize_buff_threshhold - radius), 5) / 50.0
        self.norm_start = [float(self.ho.pos[0]) * self.scaling_factor, float(self.ho.pos[1]) * self.scaling_factor]

        self.norm_end = self.norm_start
        # Calculate speed
        self.calculate_strain(prev, 0)
        # Calculate aim
        self.calculate_strain(prev, 1)

    def calculate_strain(self, prev, diff_type: int):
        if prev == None:
            return
        res = 0
        time_elapsed = int(self.ho.time) - int(prev.ho.time)
        decay = math.pow(decay_base[diff_type], time_elapsed / 1000.0)
        scaling = weight_scaling[diff_type]
        if self.ho.h_type in (1, 2):
            dis = math.sqrt(
                math.pow(self.norm_start[0] - prev.norm_end[0], 2) + math.pow(self.norm_start[1] - prev.norm_end[1], 2))
            res = self.spacing_weights(dis, diff_type) * scaling
        res /= max(time_elapsed, 50)
        self.strains[diff_type] = prev.strains[diff_type] * decay + res

    def spacing_weights(self, distance: float, diff_type: int):
        if diff_type == 0:
            if distance > single_spacing:
                return 2.5
            elif distance > stream_spacing:
                return 1.6 + 0.9 * (distance - stream_spacing) / (single_spacing - stream_spacing)
            elif distance > almost_diameter:
                return 1.2 + 0.4 * (distance - almost_diameter) / (stream_spacing - almost_diameter)
            elif distance > (almost_diameter / 2.0):
                return 0.95 + 0.25 * (distance - almost_diameter / 2.0) / (almost_diameter / 2.0)
            else:
                return 0.95
        elif diff_type == 1:
            return math.pow(distance, 0.99)
        else:
            return 0.0


def calculate_difficulty(btmap: Beatmap, type, objects, radius):
    strain_step = 400
    prev = None
    max_strain = 0
    decay_weight = 0.9
    highest_strains = []
    interval_end = strain_step
    for obj in btmap.hit_objects:
        new = DiffObj(obj, radius, prev)
        objects.append(new)
        while int(new.ho.time) > interval_end:
            highest_strains.append(max_strain)
            if prev == None:
                max_strain = 0
            else:
                decay = math.pow(decay_base[type], (interval_end - int(prev.ho.time)) / 1000.0)
                max_strain = prev.strains[type] * decay
            interval_end += strain_step
        prev = new
        max_strain = max(new.strains[type], max_strain)
    difficulty = 0
    weight = 1.0
    highest_strains = sorted(highest_strains, reverse=True)
    for strain in highest_strains:
        difficulty += weight * strain
        weight *= decay_weight
    return difficulty


def main(btmap: Beatmap):
    objects = []
    radius = (512 / 16) * (1.0 - 0.7 * (btmap.cs - 5) / 5)

    aim = calculate_difficulty(btmap, 1, objects, radius)
    speed = calculate_difficulty(btmap, 0, objects, radius)
    aim = math.sqrt(aim) * star_scaling_factor
    speed = math.sqrt(speed) * star_scaling_factor

    stars = aim + speed + abs(speed - aim) * extreme_scaling_factor
    return [aim, speed, stars, btmap]
