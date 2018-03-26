import time
from function import bot_IOfile
from function import bot_osu
from center import bot_global


# 适用群列表: 分群，喵呜，要饭，队群
group_list = [514661057, 326389728, 641236878, 693657455]


def JobCenter(bot, maxcount):
	count = 0
	while count < maxcount:
		print('定时任务启动')
		if bot_global.bp_watch:
			count = count + 1
			msg = '开始查询BP\n本次为bot启动后第%s次查询' % count
			print(msg)
			bot_global.user_bp_list_lock.acquire()
			for num in range(len(bot_global.user_bp_list)):
				user = bot_global.user_bp_list[num]
				user_id = user[20]["user_id"]
				score_mode = user[20]["user_mode"]
				new_bp = bot_osu.get_bp(user_id, score_mode)
				if new_bp:
					for i in range(0, 20):
						if new_bp[i] != user[i]:
							msg = '某人bp%s有变化,但是细节查询失败,将等待至下次查询' % (i+1)
							(a1, user_name, a3, a4, a5, a6) = bot_osu.get_info(user_id, score_mode, type_mode='id')
							mode_name = bot_osu.get_mode(score_mode)
							if float(user[i]["pp"]) > float(new_bp[i]["pp"]):
								map_id = user[i]["beatmap_id"]
								map_info = bot_osu.get_map(map_id, score_mode)
								score_mod = bot_osu.get_mod(user[i]["enabled_mods"])
								old_pp = float(user[i]["pp"])
								new_pp = float(bot_osu.get_map_pp(user_id, map_id, score_mode))
								if user_name and map_info and new_pp:
									msg = '%s倒刷了一张图 (%s)\n谱面bid: %s\n%s\nMod: %s\n倒刷前的pp: %.2f\n现在的pp: %.2f'\
										% (user_name, mode_name, map_id, map_info, score_mod, old_pp, new_pp)
									update_bp = new_bp[0:20]
									update_bp.append({"user_id": user_id, "user_name": user_name, "user_mode": score_mode})
									bot_global.user_bp_list[num] = update_bp
									bot_IOfile.write_pkl_data(bot_global.user_bp_list, 'D:\Python POJ\lxybot_v2\data\data_bp_care_list.pkl')
							else:
								map_id = new_bp[i]["beatmap_id"]
								map_info = bot_osu.get_map(map_id, score_mode)
								score_rank = bot_osu.get_rank(new_bp[i]["rank"])
								score_acc = bot_osu.get_acc(new_bp[i]["count300"], new_bp[i]["count100"], new_bp[i]["count50"], new_bp[i]["countmiss"])
								score_mod = bot_osu.get_mod(new_bp[i]["enabled_mods"])
								score_pp = float(new_bp[i]["pp"])
								if user_name and map_info:
									msg = '%s更新了bp%s (%s)\n谱面bid: %s\n%s\n评分: %s\nAcc: %s%%\nMod: %s\npp: %.2f'\
										% (user_name, i+1, mode_name, map_id, map_info, score_rank, score_acc, score_mod, score_pp)
									update_bp = new_bp[0:20]
									update_bp.append({"user_id": user_id, "user_name": user_name, "user_mode": score_mode})
									bot_global.user_bp_list[num] = update_bp
									bot_IOfile.write_pkl_data(bot_global.user_bp_list, 'D:\Python POJ\lxybot_v2\data\data_bp_care_list.pkl')
							for group in group_list:
								bot.send_group_msg(group_id=group, message=msg)
							break
			bot_global.user_bp_list_lock.release()
			print('本轮查询结束')
			time.sleep(300)
		else:
			time.sleep(60)
