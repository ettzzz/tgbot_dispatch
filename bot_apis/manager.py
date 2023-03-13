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
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from configs.private_vars import BOT_INFO
from .v2ray_update.nice_scrapper import call_nice_scrapper
from .weather_query.weather_reminder import call_weather_reminder
from .nga_bargain.apis import (
    call_read_bargains,
    call_read_keywords,
    call_next_bargains,
    call_prev_bargains,
    call_end_bargains,
)
from .maedchen_ai.apis import (
    call_ai_reboot,
    call_ai_sleep,
    call_ai_wakeup,
    call_ai_chat,
)


async def helloworld(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo!")


def create_interactive_updater():
    is_interactive = 1
    token = BOT_INFO[is_interactive]["api_token"]

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("hi", helloworld))
    application.add_handler(CommandHandler("v2ray", call_nice_scrapper))
    application.add_handler(CommandHandler("wetter", call_weather_reminder))
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("bargain", call_read_keywords)],
            states={
                0: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, call_read_bargains),
                    CallbackQueryHandler(call_next_bargains, pattern="^n"),
                    CallbackQueryHandler(call_prev_bargains, pattern="^p"),
                    CallbackQueryHandler(call_end_bargains, pattern="^e$"),
                ],
            },
            fallbacks=[CommandHandler("bargain", call_read_keywords)],
        )
    )
    application.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("wake", call_ai_wakeup),
                CommandHandler("reboot", call_ai_reboot),
            ],
            states={
                0: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, call_ai_chat),
                    CommandHandler("reboot", call_ai_reboot),
                ],
                ConversationHandler.TIMEOUT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, call_ai_sleep)
                ],  ## TODO: it's not behavioring as I expected, remain untouched
            },
            fallbacks=[CommandHandler("sleep", call_ai_sleep)],
            conversation_timeout=0,  ## No timeout at all
        )
    )
    application.run_polling()


def create_automatic_updater():
    is_interactive = 0
    token = BOT_INFO[is_interactive]["api_token"]

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("hi", helloworld))

    application.run_polling()
