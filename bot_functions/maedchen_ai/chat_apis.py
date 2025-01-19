#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:30:13 2023

@author: eee
"""
from telegram.ext import ContextTypes
from telegram import Update

from llm_functions.chat_api import deepseekChat as ChatAgent


chat_systemprompt = """
You are a language teacher that will teach the learner about the knowledge of a foreign language. You can consider the native language of learner is English and Chinese.
"""

chat_agent = ChatAgent(system_prompt=chat_systemprompt.strip())


async def reboot_chat(update, context):
    chat_agent.reset_messages()
    await update.message.reply_text("What's in your mind?")
    return 0


async def call_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("Thinking...")
    reply = chat_agent.chat(query)
    try:
        await update.message.reply_text(reply, parse_mode="Markdown")
    except:
        await update.message.reply_text(reply) ## it seems telegram bot cannot parse "_" in markdown
    return 0

