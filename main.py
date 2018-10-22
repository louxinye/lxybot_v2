# -*- coding: utf-8 -*-
import threading
from cqhttp import CQHttp
from center import bot_msg
from center import bot_job
from center import bot_req


bot = CQHttp(api_root='http://127.0.0.1:5700/')


@bot.on_message()
def handle_msg(context):
    t1 = threading.Thread(target=bot_msg.MsgCenter, args=(bot, context))
    t1.start()


@bot.on_request()
def handle_request(context):
    t2 = threading.Thread(target=bot_req.ReqCenter, args=(bot, context))
    t2.start()


# bp监视定时任务
max_count = 5000
sched_t1 = threading.Thread(target=bot_job.bpCareCenter, args=(bot, max_count))
sched_t1.setDaemon(True)
sched_t1.start()

# 踢人定时任务
sched_t2 = threading.Thread(target=bot_job.killCenter, args=(bot,))
sched_t2.setDaemon(True)
sched_t2.start()

# pp超限踢人定时任务
sched_t3 = threading.Thread(target=bot_job.checkOutCenter, args=(bot,))
sched_t3.setDaemon(True)
sched_t3.start()

# 记录清除定时任务
sched_t4 = threading.Thread(target=bot_job.cleanCenter, args=(bot,))
sched_t4.setDaemon(True)
sched_t4.start()


# 监听启动
bot.run(host='127.0.0.1', port=8912)
