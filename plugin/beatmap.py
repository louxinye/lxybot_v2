import math
import configparser
from plugin.map_types import HitObject, TimingPoint, SliderData

class Beatmap:
    # Slots are used to optimize memory usage
    __slots__ = ('data', 'title', 'artist', 'creator', 'version', 'hp',
                 'cs', 'od', 'ar', 'sm', 'tick_rate', 'num_circles',
                 'num_sliders', 'num_spinners', 'max_combo', 'num_objects',
                 'hit_objects', 'ho_num', 'timing_points', 'tp_num', 'tp_sec',
                 'ho_sec', 'valid', 'basic_cfg')

    def __init__(self, data):
        # Combo
        self.num_circles = 0
        self.num_sliders = 0
        self.num_spinners = 0
        self.max_combo = 0
        self.num_objects = 0

        self.hit_objects = []
        self.ho_num = 0

        # Timing points
        self.timing_points = []
        self.tp_num = 0

        # Some init variables
        self.tp_sec = False
        self.ho_sec = False
        self.valid = True
        self.basic_cfg = configparser.ConfigParser()

        splitted = data.split("[Events]")
        # if there's Events section
        if len(splitted) > 1:
            self.data = "[Events]\n"
            # Remove first line from string, and convert it
            # from list back to string without first element
            # Maybe there's a nicer way, but I don't know :(
            cfg_data = '\n'.join(splitted[0].splitlines()[1:])
            self.data += splitted[1]
        # if there's no Events section, let's try to split by TimingPoints sec.
        elif len(splitted) == 1:
            self.data = "[TimingPoints]\n"
            splitted = data.split("[TimingPoints]")
            # Same as above
            cfg_data = '\n'.join(splitted[0].splitlines()[1:])
            self.data += splitted[1]
        else:
            self.valid = False
            return
        self.basic_cfg.read_string(cfg_data)
        self.data = self.data.splitlines()

        # General and editor sections are not used yet
        # maybe they will be useful in future
        general = self.basic_cfg['General']
        editor = self.basic_cfg['Editor']
        metadata = self.basic_cfg['Metadata']
        diff = self.basic_cfg['Difficulty']

        # Metadata
        # use unicode title if available
        self.title = metadata.get('TitleUnicode', metadata['Title'])
        self.artist = metadata['Artist']
        self.creator = metadata['Creator']
        self.version = metadata['Version']

        # Difficulty
        self.hp = diff.getfloat('HPDrainRate')
        self.cs = diff.getfloat('CircleSize')
        self.od = diff.getfloat('OverallDifficulty')
        self.ar = diff.getfloat('ApproachRate')
        self.sm = diff.getfloat('SliderMultiplier')
        self.tick_rate = diff.getfloat('SliderTickRate')

    # Parse the timing point object
    def parse_tp(self, line):
        temp_tp = line.split(",")
        if temp_tp[0]:
            if len(temp_tp) < 3:
                self.timing_points.append(TimingPoint(temp_tp[0], temp_tp[1], 0))
            else:
                self.timing_points.append(TimingPoint(temp_tp[0], temp_tp[1], temp_tp[6]))

    # Parse the HitObject. This may take a while
    def parse_ho(self, line):
        # Start to global stuff. Need to learn more about this
        # Split commas for each line which should be a hit object
        temp_tp = line.split(",")
        if not temp_tp[0]:
            # If line is empty, we won't process it
            return
        # Set variables to send to hit object
        pos = [temp_tp[0], temp_tp[1]]
        time = temp_tp[2]
        h_type = temp_tp[3]
        end_time = 0
        slider = 0
        slider_true = 0
        if len(line.split("|")) > 1:
            slider_true = 1

        # Circle type
        if h_type == "1" or h_type == "5" or not slider_true and int(h_type) > 12:
            self.num_circles += 1
            h_type = 1
        # Slider type. Need to do some more math on sliders
        elif h_type == "2" or h_type == "6" or slider_true:
            self.num_sliders += 1
            h_type = 2
            pos_s = []
            # split into pipeline for slider logic
            sl_line = line.split("|")
            sl_type, *sl_line = sl_line
            counter = 0
            # add first slider point
            pos_s.append(pos)
            # iterate line for the rest of the slider points
            for l_pos in sl_line:
                curve = l_pos.split(":")
                pos_s.append([curve[0], curve[1].split(",")[0]])
                if len(l_pos.split(",")) > 2:
                    break
            repeats = int(l_pos.split(",")[1])
            length = float(l_pos.split(",")[2])
            time_p = None
            parent = None
            for tp in self.timing_points:
                if float(tp.time) > float(time):
                    break
                time_p = tp
            # Get the parent point
            for tp in self.timing_points:
                if int(tp.inherited) == 1:
                    parent = tp
                if tp == time_p:
                    break
            # Begin to calculte the amount of ticks for max combo
            sv_mult = 1
            if time_p.inherited == "0" and float(tp.ms_per_beat) < 0:
                sv_mult = (-100.0 / float(time_p.ms_per_beat))
            px_per_beat = self.sm * 100.0 * sv_mult
            num_beats = (length * repeats) / px_per_beat
            duration = math.ceil(num_beats * float(parent.ms_per_beat))
            end_time = float(time) + duration
            slider = SliderData(sl_type, pos_s, repeats, length)
            ticks = math.ceil((num_beats - 0.1) / repeats * self.tick_rate)
            ticks -= 1
            raw_ticks = ticks
            ticks *= repeats
            ticks += repeats + 1
            self.max_combo += ticks - 1

        # Spinner type.
        elif h_type == "8" or h_type == "12":
            self.num_spinners += 1
            h_type = 3
        else:
            print("HELP " + h_type)
            print(temp_tp)
        self.num_objects += 1
        self.max_combo += 1
        self.hit_objects.append(HitObject(pos, time, h_type, end_time, slider))

    def parse(self):
        # Begin to parse beatmap
        for line in self.data:
            # Section for timing points
            if "Mode: 1" in line or "Mode: 2" in line or "Mode: 3" in line:
                self.valid = False
                break
            if "[HitObjects]" in line:
                self.ho_sec = True
                continue
            if "[TimingPoints]" in line:
                self.tp_sec = True
                continue
            if self.tp_sec:
                self.parse_tp(line)
                self.tp_num += 1
            if self.ho_sec:
                self.parse_ho(line)
                self.ho_num += 1
            if self.tp_sec:
                self.tp_sec = False
        if not self.valid:
            return False
        else:
            return True

    def apply_mods(self, mods):
        # Ugly shouldput somewhere else
        od0_ms = 79.5
        od10_ms = 19.5
        ar0_ms = 1800
        ar5_ms = 1200
        ar10_ms = 450

        od_ms_step = 6.0
        ar_ms_step1 = 120.0
        ar_ms_step2 = 150.0

        # If no mods affecting beatmap values are used
        # FL, SO, NF
        if not mods.map_changing:
            return

        speed = 1

        if mods.dt or mods.nc:
            speed *= 1.5

        if mods.ht:
            speed *= 0.75

        od_multiplier = 1
        if mods.hr:
            od_multiplier *= 1.4
        if mods.ez:
            od_multiplier *= 0.5

        self.od *= od_multiplier
        odms = od0_ms - math.ceil(od_ms_step * self.od)

        ar_multiplier = 1

        if mods.hr:
            ar_multiplier = 1.4

        if mods.ez:
            ar_multiplier = 0.5

        self.ar *= ar_multiplier

        arms = (ar0_ms - ar_ms_step1 * self.ar) if self.ar <= 5 else (ar5_ms - ar_ms_step2 * (self.ar - 5))

        cs_multipier = 1

        if mods.hr:
            cs_multipier = 1.3

        if mods.ez:
            cs_multipier = 0.5

        odms = min(od0_ms, max(od10_ms, odms))
        arms = min(ar0_ms, max(ar10_ms, arms))

        odms /= speed
        arms /= speed

        self.od = (od0_ms - odms) / od_ms_step

        self.ar = ((ar0_ms - arms) / ar_ms_step1) if self.ar <= 5.0 else (5.0 + (ar5_ms - arms) / ar_ms_step2)
        self.cs *= cs_multipier
        self.cs = max(0.0, min(10.0, self.cs))

        if not mods.speed_changing:
            # not speed-modifying
            return

        for tp in self.timing_points:
            tp.time = float(tp.time) / speed
            if int(tp.inherited) == 0:
                tp.ms_per_beat = float(tp.ms_per_beat) / speed

        for obj in self.hit_objects:
            obj.time = float(obj.time) / speed
            obj.end_time /= speed
