#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:30:13 2023

@author: eee
"""

from telegram.ext import ContextTypes
from telegram import Update
from bot_apis.maedchen_ai.agent_sb import ChatGPTAgent

agent = ChatGPTAgent()

GPT3_5_ROUTES, GPT4_ROUTES = range(2)  # Stages 0, 1

async def call_ai_reboot(update, context):
    from_chatgpt = agent.start()
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT3_5_ROUTES


async def call_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_user = update.message.text
    from_chatgpt = agent.chat(from_user)
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT3_5_ROUTES


async def call_ai_reboot4(update, context):
    from_chatgpt = agent.start(model="gpt-4")
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT4_ROUTES


async def call_ai_chat4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_user = update.message.text
    from_chatgpt = agent.chat(from_user, model="gpt-4")
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return GPT4_ROUTES