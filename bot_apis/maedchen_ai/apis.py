#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:30:13 2023

@author: eee
"""

from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update
from bot_apis.maedchen_ai.agent import ChatGPTAgent

agent = ChatGPTAgent()

START_ROUTES, END_ROUTES = range(2)  # Stages 0, 1


async def call_ai_wakeup(update, context):
    chat_id = update.message.chat_id
    from_chatgpt = agent.reload(chat_id)
    await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    return START_ROUTES


async def call_ai_sleep(update, context):
    chat_id = update.message.chat_id
    agent.teabreak(chat_id)
    await update.message.reply_text("Sleeping...I will see you around.")
    return ConversationHandler.END


async def call_ai_reboot(update, context):
    chat_id = update.message.chat_id
    from_chatgpt = agent.restart(chat_id)
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return START_ROUTES


async def call_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_user = update.message.text
    from_chatgpt = agent.chat(from_user)
    try:
        await update.message.reply_text(from_chatgpt, parse_mode="Markdown")
    except:
        await update.message.reply_text(from_chatgpt) ## it seems telegram bot cannot parse "_" in markdown
    return START_ROUTES

