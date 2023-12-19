#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 16:02:12 2023

@author: eee
"""

import os

import pandas as pd
from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from configs.static_vars import ROOT
from bot_apis.nga_bargain.scrapper import ngaBargainScrapper
from utils.datetime_tools import get_delta_date


dir_path = os.path.join(ROOT, "_barnhouse")
START_ROUTES, END_ROUTES = range(2)  # Stages 0, 1
STEP = 5
file_name = "ngabargainpair.csv"

def read_tid():
    file_path = os.path.join(dir_path, file_name)
    if not os.path.exists(file_path):
        return None
    df = pd.read_csv(file_path)
    return df.iloc[len(df)-1]["tid"]

def save_bargains(pair, date, tid, days_backward=3):
    file_path = os.path.join(dir_path, file_name)
    df = pd.DataFrame(pair, columns = ["desc", "link"])
    df["date"] = date
    df["tid"] = tid
    if os.path.exists(file_path):
        prev_df = pd.read_csv(file_path)
    df = pd.concat([prev_df, df])
    
    edge_date = get_delta_date(date, days_backward*(-1))
    df = df[df["date"] >= edge_date]
    df.to_csv(file_path, index=False)
    
def read_bargains(keywords):
    file_path = os.path.join(dir_path, file_name)
    pairs = set()
    df = pd.read_csv(file_path)
    for idx, row in df.iterrows():
        if any(k.strip() in row["desc"] for k in keywords):
            pairs.add((row["desc"], row["link"]))
    
    return list(pairs), row["date"]

def generate_md_text(buylist, idx=0, step=STEP):
    keywords = buylist.split(" ")
    bargains, _ = read_bargains(keywords)
    total = len(bargains)

    start = min(idx, idx + step)
    end = max(idx, idx + step)
    if start <= 0:
        start = 0
        end = abs(step)
    if start > total - 1:
        start = total - total % step
        end = total

    if total == 0:
        md_text = "暂无此商品打折记录"
    else:
        md_text = f"当前显示{start+1}/{total}个商品\n"
        for title, link in bargains[start:end]:
            md_text += "\n"
            md_text += f"{title}({link})\n"

    return md_text, start


def call_nga_bargain_scrapper():
    tid = read_tid()
    nga_scrapper = ngaBargainScrapper(tid=tid)
    r = nga_scrapper.get_raw()
    if r is None:
        return  # something wrong, TODO: gibber say something
    pair, date, tid = nga_scrapper.data_clean(r)
    if len(pair) == 0:
        return  # something wrong, TODO: gibber say something
    save_bargains(pair, date, tid, days_backward=3)


async def call_read_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好！请输入打折商品关键词，多个请用空格隔开。")
    return START_ROUTES


async def call_read_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buylist = update.message.text
    buylist.replace(",", " ").replace("，", " ")

    md_text, _ = generate_md_text(buylist=buylist, idx=0, step=STEP)

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data=f"p|{buylist}|0"),
            InlineKeyboardButton("next", callback_data=f"n|{buylist}|0"),
            InlineKeyboardButton("end", callback_data="e"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(md_text, reply_markup=reply_markup)
    return START_ROUTES


async def call_next_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _mark, buylist, prev_start = query.data.split("|")
    start = int(prev_start) + STEP
    md_text, start = generate_md_text(buylist=buylist, idx=start, step=STEP)

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data=f"p|{buylist}|{start}"),
            InlineKeyboardButton("next", callback_data=f"n|{buylist}|{start}"),
            InlineKeyboardButton("end", callback_data="e"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=md_text, reply_markup=reply_markup)
    return START_ROUTES


async def call_prev_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _mark, buylist, prev_start = query.data.split("|")
    start = int(prev_start) - STEP
    md_text, start = generate_md_text(buylist=buylist, idx=start, step=STEP)

    keyboard = [
        [
            InlineKeyboardButton("prev", callback_data=f"p|{buylist}|{start}"),
            InlineKeyboardButton("next", callback_data=f"n|{buylist}|{start}"),
            InlineKeyboardButton("end", callback_data="e"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=md_text, reply_markup=reply_markup)
    return START_ROUTES


async def call_end_bargains(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="欢迎下次再来~")
    return ConversationHandler.END
