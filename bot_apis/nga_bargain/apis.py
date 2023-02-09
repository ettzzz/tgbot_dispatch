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
START_ROUTES, END_ROUTES = range(2) # Stages 0, 1
STEP = 5

def save_bargains(pair, date):
    file_name = f"ngabargainpair_{date}.txt"
    with open(os.path.join(dir_path, file_name), "w") as f:
        for title, link in pair:
            f.write(f"{title}|{link}\n")


def read_bargains(keywords):
    pairs = list()
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



def generate_md_text(buylist, idx=0, step=STEP):
    keywords = buylist.split(" ")
    bargains, _ = read_bargains(keywords)
    total = len(bargains)

    start = min(idx, idx+step)
    end = max(idx, idx+step)
    if start <= 0:
        start = 0
        end = abs(step)
    if start == total - 1:
        start = total - total%step
        end = total - 1

    md_text = f"当前显示{idx+1}/{total}个商品\n"
    for title, link in bargains[start:end]:
        md_text += "\n"
        md_text += f"{title}({link})\n"
        
    return md_text


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


async def call_read_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hey！请输入商品关键词，用空格隔开。")
    return START_ROUTES


async def call_read_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buylist = update.message.text
    buylist.replace(",", " ").replace("，", " ")

    md_text = generate_md_text(buylist=buylist, idx=0, step=STEP)

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data=f"p|{buylist}|0"),
            InlineKeyboardButton("next", callback_data=f"n|{buylist}|0"),
            InlineKeyboardButton("end", callback_data="e"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(md_text, reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES
    


async def call_next_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _mark, buylist, start = query.data.split("|")
    md_text = generate_md_text(buylist=buylist, idx=start, step=STEP)

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data=f"p|{buylist}|{start}"),
            InlineKeyboardButton("next", callback_data=f"n|{buylist}|{start}"),
            InlineKeyboardButton("end", callback_data="e"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(md_text, reply_markup=reply_markup)
    return START_ROUTES


async def call_prev_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _mark, buylist, start = query.data.split("|")
    md_text = generate_md_text(buylist=buylist, idx=start, step=-STEP)

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data=f"p|{buylist}|{start}"),
            InlineKeyboardButton("next", callback_data=f"n|{buylist}|{start}"),
            InlineKeyboardButton("end", callback_data="e"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(md_text, reply_markup=reply_markup)
    return START_ROUTES


async def call_end_bargains(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    return ConversationHandler.END

