#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 15:45:42 2021

@author: eee
"""

import os
import datetime

import requests
from telegram.ext import CallbackContext
from telegram import Update

from config.static_vars import BASE_HEADERS, ROOT


def call_baipiaov2ray(update: Update, _: CallbackContext):  # _ is a must...
    today = datetime.datetime.today()
    yesterday = today + datetime.timedelta(-1)
    today_str = "%02d" % today.month + "%02d" % today.day
    yesterday_str = "%02d" % yesterday.month + "%02d" % yesterday.day
    today_url = (
        "https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/{}.txt".format(
            today_str
        )
    )
    yesterday_url = (
        "https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/{}.txt".format(
            yesterday_str
        )
    )
    try:
        rt = requests.get(url=today_url, headers=BASE_HEADERS, timeout=5)
        ry = requests.get(url=yesterday_url, headers=BASE_HEADERS, timeout=5)
        if not rt.text.startswith("404"):
            text = "白嫖v2ray{}更新啦！".format(today_str)
            link = today_url
            with open(os.path.join(ROOT, "barnhouse", "latest_v2ray.txt"), "w") as f_in:
                f_in.write(rt.text)
        elif not ry.text.startswith("404"):
            text = "白嫖v2ray{}更新啦！".format(yesterday_str)
            link = yesterday_url
            with open(os.path.join(ROOT, "barnhouse", "latest_v2ray.txt"), "w") as f_in:
                f_in.write(ry.text)
        else:
            text = "今天并没有可以白嫖的"
            link = "/"
    except:
        text = "淦 requests出错了，赶紧debug"
        link = "/"

    html_text = '<a href="{}">{}</a>'.format(link, text)
    update.message.reply_html(html_text, disable_web_page_preview=True)
