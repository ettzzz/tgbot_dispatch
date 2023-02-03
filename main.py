#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:07:00 2022

@author: eee
"""

import os
from apscheduler.schedulers.background import BackgroundScheduler

from fastapi import FastAPI
from pydantic import BaseModel

from configs.static_vars import API_PREFIX, DEBUG, ROOT

_private_var_path = os.path.join(ROOT, "configs", "private_vars.py")
assert os.path.exists(_private_var_path), "Woo! You missed private_vars.py~"
from configs.private_vars import BOT_INFO
from bot_apis import *


app = FastAPI(debug=DEBUG)
scheduler = BackgroundScheduler()


def automatic_forward_message(text, link="", is_interactive=0):
    bot_config = BOT_INFO[is_interactive]
    res = call_messager(
        api_token=bot_config["api_token"],
        chat_id=bot_config["chat_id"],
        message_text=text,
        message_link=link,
    )
    return res


@app.on_event("startup")
def init_scheduler():
    scheduler.add_job(
        func=call_nga_bargain_scrapper,
        trigger="cron",
        hour=23,
    )
    scheduler.start()


@app.get(f"/{API_PREFIX}/helloworld")
def call_helloworld():
    return test_hello_world()


@app.get(f"/{API_PREFIX}/latest_v2ray")
def call_latest_v2ray():
    return call_get_latest_v2ray_file()


class postCallSendMessage(BaseModel):
    is_ai: int
    text: str
    link: str


@app.post(f"/{API_PREFIX}/send_message")
def call_send_message(item: postCallSendMessage):
    is_interactive = 0 if item.is_ai == 0 else 1  ## default should be probius
    text = item.text
    link = item.link
    return automatic_forward_message(text, link, is_interactive)
