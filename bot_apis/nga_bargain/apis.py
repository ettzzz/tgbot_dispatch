#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 16:02:12 2023

@author: eee
"""

import os

from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

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
                try:
                    title, link = r.split("|")
                    if any(k in title for k in keywords):
                        temp.append((title, link))
                except:
                    continue
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



def generate_md_text(buylist, idx=0, step=5, save_keywords=False):
    keywords = buylist.split(" ")
    if save_keywords is True:
        save_keywords(keywords)
    bargains, _ = read_bargains(keywords)

    if idx <= 0:
        idx = 0
    if idx >= len(bargains):
        idx = len(bargains) - 1

    start = min(idx, idx+step)
    end = max(idx, idx+step)
    # if start < abs(step): # lock down to first page
    #     start = 0
    #     end = abs(step)

    md_text = f"当前显示{idx+1}/{len(bargains)}个商品\n"
    for title, link in bargains[start:end]:
        md_text += f"**[{title}]({link})**\n"
        md_text += "\n"

    return buylist, md_text, len(bargains)


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


START_ROUTES, END_ROUTES = range(2) # Stages 0, 1


async def call_read_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    previous_keywords = read_keywords()
    p = " ".join(previous_keywords)
    text = f"hey！请输入商品关键词，用空格隔开。\n上次关键词为：{p}"
    await update.message.reply_text(text)
    return START_ROUTES


async def call_read_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buylist = update.message.text
    buylist.replace(",", " ").replace("，", " ")

    _, md_text, total = generate_md_text(buylist=buylist, idx=0, step=5, save_keywords=True)

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data=f"p|{md_text}|{total}"),
            InlineKeyboardButton("next", callback_data=f"n|{md_text}|{total}"),
            InlineKeyboardButton("end", callback_data="e"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        md_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES
    # return ConversationHandler.END


async def call_next_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data="p|text|cid|ttp|ttc"),
            InlineKeyboardButton("next", callback_data="n|text|cid|ttp|ttc"),
            InlineKeyboardButton("end", callback_data="e|text|cid|ttp|ttc"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="next page", reply_markup=reply_markup)

    return START_ROUTES


async def call_prev_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="prev page")
    return START_ROUTES
    # if?


async def call_end_bargains():
    return


async def call_bargain_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="下次再来")

    return ConversationHandler.END
