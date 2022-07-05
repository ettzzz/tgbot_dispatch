#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:52:16 2022

@author: eee
"""


import os

import requests
from telegram.ext import CallbackContext
from telegram import Update

from configs.static_vars import UA, ROOT
from utils.datetime_tools import get_today_date, get_delta_date


def _check_github_raw(date):
    """
    date STR standard date e.g. 2022-07-05
    """
    headers = {"User-Agent": UA}
    len4date = "".join(date.split("-")[1:])
    url = f"https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/{len4date}.txt"
    try:
        r = requests.get(url, headers=headers, timeout=5)
    except:
        return None  ## timeout

    return r


def call_nice_scrapper(update: Update, _: CallbackContext):  # _ is a must...
    today = get_today_date()
    text = "现在并没有可以白嫖的"
    for i in range(4):  ## check last 3 days:
        date = get_delta_date(today, days=-1 * i)
        r = _check_github_raw(date)
        if r is not None and r.status_code == 200:
            with open(os.path.join(ROOT, "_barnhouse", "v2ray.txt"), "w") as f:
                f.write(r.text)
            text = f"白嫖v2ray{date}更新啦！"
            break
        else:
            continue

    html_text = f'<a href="">{text}</a>'
    update.message.reply_html(html_text, disable_web_page_preview=True)


def call_get_latest_v2ray_file():
    _path = os.path.join(ROOT, "_barnhouse", "v2ray.txt")
    if os.path.exists(_path):
        with open(_path, "r") as f:
            r = f.read()
        return r
    else:
        return ""
