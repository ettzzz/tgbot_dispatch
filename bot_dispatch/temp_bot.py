# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:55:29 2021

@author: ert
"""


import logging
import datetime

import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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
    

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
browser_headers = {
    'User-Agent': ua, 
    }

    
def baipiaov2ray(update: Update, _: CallbackContext): # _ is a must...
    today = datetime.datetime.today()
    ymd = str(today.year) + '%02d' % today.month + '%02d' % today.day
    date_str = ymd[4:]
    base_url = 'https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/{}.txt'.format(date_str)
    
    r = requests.get(
        url = base_url,
        headers = browser_headers,
        timeout = 5
        )
        
    if r.text.startswith('404'):
        text = '今天并没有可以白嫖的'
        link = ''
    else:
        text = '白嫖v2ray{}更新啦！'.format(date_str)
        link = base_url
    
    html_text = '<a href="{}">{}</a>'.format(link, text)
    update.message.reply_html(html_text, disable_web_page_preview=True)


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater('966629533:AAFJOn_J_EDEQZPcRftHdSEHHu38PtGxrPI')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("v2ray", baipiaov2ray))
    # TODO:
        # raining bot /rain
        # stock bot

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()