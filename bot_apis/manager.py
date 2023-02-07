#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 15:20:41 2023

@author: eee
"""


from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
)

from configs.private_vars import BOT_INFO
from .v2ray_update.nice_scrapper import call_nice_scrapper
from .weather_query.weather_reminder import call_weather_reminder
from .nga_bargain.apis import call_read_bargains, call_read_keywords


async def helloworld(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo!")


def create_interactive_updater():
    is_interactive = 1
    token = BOT_INFO[is_interactive]["api_token"]

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("hi", helloworld))
    application.add_handler(CommandHandler("v2ray", call_nice_scrapper))
    application.add_handler(CommandHandler("wetter", call_weather_reminder))
    # application.add_handler(CommandHandler("newbkey", helloworld))
    # application.add_handler(CommandHandler("curbkey", call_read_keywords))
    application.add_handler(CommandHandler("bargain", call_read_bargains))

    application.run_polling()


def create_automatic_updater():
    is_interactive = 0
    token = BOT_INFO[is_interactive]["api_token"]

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("hi", helloworld))

    application.run_polling()
