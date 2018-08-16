class Mods:
    __slots__ = ('map_changing', 'nf', 'ez', 'hd', 'hr', 'dt', 'ht', 'nc',
                 'fl', 'so', 'speed_changing', 'map_changing')

    def __init__(self, mods_str=''):
        self.nf = False
        self.ez = False
        self.hd = False
        self.hr = False
        self.dt = False
        self.ht = False
        self.nc = False
        self.fl = False
        self.so = False
        self.speed_changing = False
        self.map_changing = False
        if mods_str:
            self.from_str(mods_str)
        self.update_state()

    def update_state(self):
        # speed changing - dt or ht or nc is used
        self.speed_changing = self.dt or self.ht or self.nc
        # if hr or ez or dt or ht or nc
        self.map_changing = self.hr or self.ez or self.speed_changing

    def __str__(self):
        string = ''
        if self.nf:
            string += "NF"
        if self.ez:
            string += "EZ"
        if self.hd:
            string += "HD"
        if self.hr:
            string += "HR"
        if self.dt:
            string += "DT"
        if self.ht:
            string += "HT"
        if self.nc:
            string += "NC"
        if self.fl:
            string += "FL"
        if self.so:
            string += "SO"
        return string

    def from_str(self, mods):
        if not mods:
            return
        # split mods string to chunks with length of two characters
        mods = [mods[i:i + 2] for i in range(0, len(mods), 2)]
        if "NF" in mods:
            self.nf = True
        if "EZ" in mods:
            self.ez = True
        if "HD" in mods:
            self.hd = True
        if "HR" in mods:
            self.hr = True
        if "DT" in mods:
            self.dt = True
        if "HT" in mods:
            self.ht = True
        if "NC" in mods:
            self.nc = True
        if "FL" in mods:
            self.fl = True
        if "SO" in mods:
            self.so = True
        self.update_state()


class HitObject:
    __slots__ = ('pos', 'time', 'h_type', 'end_time', 'slider')

    def __init__(self, pos, time, h_type, end_time, slider):
        self.pos = pos
        self.time = time
        self.h_type = h_type
        self.end_time = end_time
        self.slider = slider


class SliderData:
    __slots__ = ('s_type', 'points', 'repeats', 'length')

    def __init__(self, s_type, points, repeats, length):
        self.s_type = s_type
        self.points = points
        self.repeats = repeats
        self.length = length


class TimingPoint:
    __slots__ = ('time', 'ms_per_beat', 'inherited')

    def __init__(self, time, ms_per_beat, inherited):
        self.time = time
        self.ms_per_beat = ms_per_beat
        self.inherited = inherited
