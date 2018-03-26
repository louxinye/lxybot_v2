# -*- coding: utf-8 -*-
import threading
from cqhttp import CQHttp
from center import bot_msg
from center import bot_job


bot = CQHttp(api_root='http://127.0.0.1:5700/')


@bot.on_message()
def handle_msg(context):
    t = threading.Thread(target=bot_msg.MsgCenter, args=(bot, context))
    t.start()


# 定时任务
maxcount = 1000
sched_t = threading.Thread(target=bot_job.JobCenter, args=(bot, maxcount))
sched_t.setDaemon(True)
sched_t.start()


# 监听启动
bot.run(host='127.0.0.1', port=8912)