#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 15:20:41 2023

@author: eee
"""

import os

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

DEBUG = os.getenv("DEBUG")
if DEBUG != "0":
    from configs.secrets import *
    
from bot_functions.maedchen_ai.chat_apis import call_chat, reboot_chat
from bot_functions.maedchen_ai.voice_apis import call_oralchat, reboot_oralchat



async def helloworld(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo! Ich bin ein Bot. Bitte sprich mit mir!")

async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sleeping...Bye!")
    return ConversationHandler.END

async def _call_ai_fallback(update, context):
    await update.message.reply_text("Triggered fallback. Conversation ends.")
    return ConversationHandler.END

BASIC_CHAT = 0
ORAL_CHAT = 1

def activate_bot():
    token = os.getenv("MAI_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("hi", helloworld))
    
    application.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("start", reboot_chat),
                CommandHandler("oral", reboot_oralchat),
            ],
            states={
                BASIC_CHAT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, call_chat),
                    CommandHandler("start", reboot_chat),
                    CommandHandler("oral", reboot_oralchat),
                    CommandHandler("end", end_conversation)
                ],
                ORAL_CHAT: [
                    MessageHandler(filters.VOICE & (~filters.COMMAND), call_oralchat),
                    CommandHandler("oral", reboot_oralchat),
                    CommandHandler("start", reboot_chat),
                    CommandHandler("end", end_conversation)
                ]
            },
            fallbacks=[MessageHandler(filters.TEXT, _call_ai_fallback)],
            # conversation_timeout=900,  # 15 minutes
        )
    )
    application.run_polling()


if __name__ == "__main__":
    activate_bot()