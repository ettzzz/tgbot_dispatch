#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 15:48:28 2021

@author: eee
"""

import re
import time
import json

import requests
from telegram.ext import CallbackContext
from telegram import Update

from config.static_vars import BASE_HEADERS, pois


def call_isitgoingtorain(update: Update, _: CallbackContext):
    base_url = "https://isitgoingtorain.com/data/forecast.php"
    r_home = requests.get(base_url, params=pois["home"], headers=BASE_HEADERS)

    r_work = requests.get(base_url, params=pois["work"], headers=BASE_HEADERS)

    useful_str_home = re.findall("initForecast[(](.*?)[)];", r_home.text)
    useful_str_work = re.findall("initForecast[(](.*?)[)];", r_work.text)

    if len(useful_str_home) > 0 and len(useful_str_work) > 0:
        now = time.localtime()

        def max_func(x):
            return x["pP"]

        forecast_home = json.loads(useful_str_home[0])
        forecast_work = json.loads(useful_str_work[0])

        todays_home = forecast_home["forecast"][0]["data"]
        tomorrows_home = forecast_home["forecast"][1]["data"]
        todays_work = forecast_work["forecast"][0]["data"]
        tomorrows_work = forecast_work["forecast"][1]["data"]

        fresh = [
            max(todays_home[7:9], key=max_func)["pP"],  # morning today
            max(todays_work[17:19], key=max_func)["pP"],  # offwork today
            max(todays_home[21:] + tomorrows_home[:7], key=max_func)[
                "pP"
            ],  # night today
            max(tomorrows_home[7:9], key=max_func)["pP"],  # morning tomorrow
            max(tomorrows_work[17:19], key=max_func)["pP"],  # offwork tomorrow
        ]

        if now.tm_hour <= 8:
            text = "今天上班下雨max p={}, 下班下雨max p={}, 晚上下雨max p={}。".format(
                fresh[0], fresh[1], fresh[2]
            )
        elif now.tm_hour <= 19 and now.tm_hour > 8:
            text = "今天下班下雨max p={}, 晚上下雨max p={}, 明天上班下雨max p={}。".format(
                fresh[1], fresh[2], fresh[3]
            )
        else:
            text = "今天睡觉下雨max p={}, 明天上班下雨max p={}, 明天下班下雨max p={}。".format(
                fresh[2], fresh[3], fresh[4]
            )
    else:
        text = "淦 requests出错了，赶紧debug"

    update.message.reply_text(text)
