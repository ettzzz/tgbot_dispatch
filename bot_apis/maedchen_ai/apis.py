#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:30:13 2023

@author: eee
"""
import os

from telegram.ext import ContextTypes
from telegram import Update
from bot_apis.maedchen_ai.agent_openai import ChatGPTAgent

agent = ChatGPTAgent()

GPT3_5_ROUTES, GPT4_ROUTES = range(2)  # Stages 0, 1
GPT3_5_MODEL = os.getenv("GPT3_5_MODEL")
GPT4_MODEL = os.getenv("GPT4_MODEL")

async def call_ai_reboot(update, context):
    from_chatgpt = agent.start(model=GPT3_5_MODEL)
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT3_5_ROUTES


async def call_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_user = update.message.text
    from_chatgpt = agent.chat(from_user, model=GPT3_5_MODEL)
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT3_5_ROUTES


async def call_ai_reboot4(update, context):
    from_chatgpt = agent.start(model=GPT4_MODEL)
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT4_ROUTES


async def call_ai_chat4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_user = update.message.text
    from_chatgpt = agent.chat(from_user, model=GPT4_MODEL)
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT4_ROUTES