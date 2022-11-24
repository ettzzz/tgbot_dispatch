# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:55:29 2021

@author: ert
"""

from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler

from configs.private_vars import BOT_INFO
from .v2ray_update.nice_scrapper import call_nice_scrapper
from .weather_query.weather_reminder import call_weather_reminder

def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def helloworld(update: Update, context: CallbackContext):
    update.message.reply_text("Hallo!")


def create_interactive_updater():
    is_interactive = 1
    updater = Updater(BOT_INFO[is_interactive]["api_token"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("hi", helloworld))
    dispatcher.add_handler(CommandHandler("v2ray", call_nice_scrapper))
    dispatcher.add_handler(CommandHandler("wetter", call_weather_reminder))

    updater.start_polling()
    # updater.idle() ## only use this when you are on a IDE and have access to Internet


def create_automatic_updater():
    is_interactive = 0
    updater = Updater(BOT_INFO[is_interactive]["api_token"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("hi", helloworld))

    updater.start_polling()
