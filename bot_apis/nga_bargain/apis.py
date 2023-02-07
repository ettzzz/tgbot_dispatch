#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 16:02:12 2023

@author: eee
"""

import os

from telegram.ext import ContextTypes
from telegram import Update

from configs.static_vars import ROOT
from bot_apis.nga_bargain.scrapper import ngaBargainScrapper
from utils.datetime_tools import struct_datestr


dir_path = os.path.join(ROOT, "_barnhouse")


def save_keywords(keywords):
    file_name = "ngabargainkeywords.txt"
    with open(os.path.join(dir_path, file_name), "w") as f:
        f.write(",".join(keywords))


def read_keywords():
    file_name = "ngabargainkeywords.txt"
    file_path = os.path.join(dir_path, file_name)
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        text = f.read()
    return text.split(",")


def save_bargains(pair, date):
    file_name = f"ngabargainpair_{date}.txt"
    with open(os.path.join(dir_path, file_name), "w") as f:
        for title, link in pair:
            f.write(f"{title}|{link}\n")


def read_bargains(keywords=None):
    pairs = list()
    if keywords is None:
        keywords = read_keywords()
    for file_name in os.listdir(dir_path):
        if file_name.startswith("ngabargainpair"):
            date = file_name.split("_")[1].split(".txt")[0]
            with open(os.path.join(dir_path, file_name), "r") as f:
                p = f.read()
            temp = list()
            for r in p.split("\n"):
                title, link = r.split("|")
                if any(k in title for k in keywords):
                    temp.append((title, link))
            pairs += temp

    return pairs, date


def _barnhouse_check(date, days_backward=3):
    struct_d = struct_datestr(date)
    for file_name in os.listdir(dir_path):
        if file_name.startswith("ngabargainpair"):
            d = file_name.split("_")[1].split(".txt")[0]
            sd = struct_datestr(d)
            if (struct_d - sd).days >= days_backward:
                file_path = os.path.join(dir_path, file_name)
                os.remove(file_path)
    return


def call_nga_bargain_scrapper():
    nga_scrapper = ngaBargainScrapper()
    r = nga_scrapper.get_raw()
    if r is None:
        return  # something wrong, TODO: gibber say something
    pair, date = nga_scrapper.data_clean(r)
    if len(pair) == 0:
        return  # something wrong, TODO: gibber say something
    save_bargains(pair, date)
    _barnhouse_check(date)


async def call_read_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text.replace(",", " ")
    text.replace("，", " ")
    keywords = read_keywords()
    print(text)
    # keywords = text.split(" ")
    # previous_keywords = read_keywords()
    # save_keywords(keywords)

    bargains = read_bargains(keywords)
    html_text = ""
    for title, link in bargains:
        html_text += f"<a href={link}>{title}</a>"
        html_text += "<br>"
    await update.message.reply_html(html_text, disable_web_page_preview=True)


async def call_read_keywords():
    return
