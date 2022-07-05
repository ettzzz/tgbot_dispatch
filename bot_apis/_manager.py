# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:55:29 2021

@author: ert
"""

from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler

from configs.private_vars import BOT_INFO
from .v2ray_update.nice_scrapper import call_nice_scrapper


def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def create_interactive_updater():
    is_interactive = 1
    updater = Updater(BOT_INFO[is_interactive]["api_token"])

    updater.dispatcher.add_handler(CommandHandler("v2ray", call_nice_scrapper))

    updater.start_polling()
    # updater.idle() ## only use this when you are on a IDE and have access to Internet


def create_automatic_updater():
    is_interactive = 0
    updater = Updater(BOT_INFO[is_interactive]["api_token"])

    # updater.dispatcher.add_handler(CommandHandler("v2ray", call_nice_scrapper))

    updater.start_polling()
