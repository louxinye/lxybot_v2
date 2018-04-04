import requests
import json
import re
from function import bot_IOfile
from function import bot_SQL
from function import bot_osu


osu_id = 10916147
osu_mode = 0
max_num = 100
a = bot_osu.getUserBp(osu_id,osu_mode,max_num=max_num)
weight = 1
total_pp = 0
for bp in a:
	total_pp = total_pp + weight * float(bp["pp"])
	weight = weight * 0.95
print(total_pp)
