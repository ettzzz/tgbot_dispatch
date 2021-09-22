# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:55:29 2021

@author: ert
"""

from telegram.ext import CallbackContext, Updater, CommandHandler
from telegram import Update

from config.static_vars import EMPLOYEE_ROSTER
from app.baipiaov2ray import call_baipiaov2ray
from app.isitgoingtorain import call_isitgoingtorain
from app.stock_manager import call_query_status, call_reset_status
from gibber import gabber

# Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)
logger = gabber

# Define a few command handlers. These usually take the two arguments update and
# context.
# def start(update: Update, _: CallbackContext) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     update.message.reply_markdown_v2(
#         fr'Hi {user.mention_markdown_v2()}\!',
#         reply_markup=ForceReply(selective=True),
#     )


# def help_command(update: Update, _: CallbackContext) -> None:
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def we_are_open() -> None:
    updater = Updater(EMPLOYEE_ROSTER["blog_notify_bot"]["api_token"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("v2ray", call_baipiaov2ray))
    dispatcher.add_handler(CommandHandler("rain", call_isitgoingtorain))
    dispatcher.add_handler(CommandHandler("status", call_query_status))
    dispatcher.add_handler(CommandHandler("reset", call_reset_status))
    # TODO: hi_there 沙雕新闻、每日戳心、每日暖心
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    # TIPS: Do NOT run this on different server
    # updater.idle()


if __name__ == "__main__":
    we_are_open()
