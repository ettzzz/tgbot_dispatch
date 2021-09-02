# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:55:29 2021

@author: ert
"""

import os
import logging
import datetime
import re
import json
import time

import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from config.static_vars import BASE_HEADERS, EMPLOYEE_ROSTER, ROOT, DQN_AGENT_HOST
from config.static_vars import pois

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
# def start(update: Update, _: CallbackContext) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     update.message.reply_markdown_v2(
#         fr'Hi {user.mention_markdown_v2()}\!',
#         reply_markup=ForceReply(selective=True),
#     )


# def help_command(update: Update, _: CallbackContext) -> None:
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


def baipiaov2ray(update: Update, _: CallbackContext):  # _ is a must...
    today = datetime.datetime.today()
    yesterday = today + datetime.timedelta(-1)
    today_str = '%02d' % today.month + '%02d' % today.day
    yesterday_str = '%02d' % yesterday.month + '%02d' % yesterday.day
    today_url = 'https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/{}.txt'.format(
        today_str)
    yesterday_url = 'https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/{}.txt'.format(
        yesterday_str)
    try:
        rt = requests.get(
            url=today_url,
            headers=BASE_HEADERS,
            timeout=5
        )
        ry = requests.get(
            url=yesterday_url,
            headers=BASE_HEADERS,
            timeout=5
        )
        if not rt.text.startswith('404'):
            text = '白嫖v2ray{}更新啦！'.format(today_str)
            link = today_url
            with open(os.path.join(ROOT, 'barnhouse', 'latest_v2ray.txt'), 'w') as f_in:
                f_in.write(rt.text)
        elif not ry.text.startswith('404'):
            text = '白嫖v2ray{}更新啦！'.format(yesterday_str)
            link = yesterday_url
            with open(os.path.join(ROOT, 'barnhouse', 'latest_v2ray.txt'), 'w') as f_in:
                f_in.write(ry.text)
        else:
            text = '今天并没有可以白嫖的'
            link = '/'
    except:
        text = '淦 requests出错了，赶紧debug'
        link = '/'

    html_text = '<a href="{}">{}</a>'.format(link, text)
    update.message.reply_html(html_text, disable_web_page_preview=True)


def isitgoingtorain(update: Update, _: CallbackContext):
    base_url = 'https://isitgoingtorain.com/data/forecast.php'
    r_home = requests.get(
        base_url,
        params=pois['home'],
        headers=BASE_HEADERS
    )

    r_work = requests.get(
        base_url,
        params=pois['work'],
        headers=BASE_HEADERS
    )

    useful_str_home = re.findall('initForecast[(](.*?)[)];', r_home.text)
    useful_str_work = re.findall('initForecast[(](.*?)[)];', r_work.text)

    if len(useful_str_home) > 0 and len(useful_str_work) > 0:
        now = time.localtime()
        def max_func(x): return x['pP']

        forecast_home = json.loads(useful_str_home[0])
        forecast_work = json.loads(useful_str_work[0])

        todays_home = forecast_home['forecast'][0]['data']
        tomorrows_home = forecast_home['forecast'][1]['data']
        todays_work = forecast_work['forecast'][0]['data']
        tomorrows_work = forecast_work['forecast'][1]['data']

        fresh = [
            max(todays_home[7:9], key=max_func)['pP'],  # morning today
            max(todays_work[17:19], key=max_func)['pP'],  # offwork today
            max(todays_home[21:] + tomorrows_home[:7], key=max_func)['pP'],  # night today
            max(tomorrows_home[7:9], key=max_func)['pP'],  # morning tomorrow
            max(tomorrows_work[17:19], key=max_func)['pP']  # offwork tomorrow
        ]

        if now.tm_hour <= 8:
            text = '今天上班下雨max p={}, 下班下雨max p={}, 晚上下雨max p={}。'.format(
                fresh[0], fresh[1], fresh[2]
            )
        elif now.tm_hour <= 19 and now.tm_hour > 8:
            text = '今天下班下雨max p={}, 晚上下雨max p={}, 明天上班下雨max p={}。'.format(
                fresh[1], fresh[2], fresh[3]
            )
        else:
            text = '今天睡觉下雨max p={}, 明天上班下雨max p={}, 明天下班下雨max p={}。'.format(
                fresh[2], fresh[3], fresh[4]
            )
    else:
        text = '淦 requests出错了，赶紧debug'

    update.message.reply_text(text)


def stock_query_status(update, _):
    r = requests.get('{}/api_v1/query_status'.format(DQN_AGENT_HOST))
    update.message.reply_text(r.json()['msg'])


def stock_reset_status(update, _):
    r = requests.get('{}/api_v1/reset_status'.format(DQN_AGENT_HOST))
    update.message.reply_text(r.json()['msg'])


def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def we_are_open() -> None:
    updater = Updater(EMPLOYEE_ROSTER['blog_notify_bot']['api_token'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("v2ray", baipiaov2ray))
    dispatcher.add_handler(CommandHandler("rain", isitgoingtorain))
    dispatcher.add_handler(CommandHandler("status", stock_query_status))
    dispatcher.add_handler(CommandHandler("reset", stock_reset_status))
    # TODO: hi_there 沙雕新闻、每日戳心、每日暖心
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    # TIPS: Do NOT run this on different server
    # updater.idle()


if __name__ == "__main__":
    we_are_open()
