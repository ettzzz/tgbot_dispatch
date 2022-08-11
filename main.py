#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:07:00 2022

@author: eee
"""

import os

from fastapi import FastAPI
from pydantic import BaseModel

from configs.static_vars import API_PREFIX, DEBUG, ROOT
assert os.path.exists(os.path.join(ROOT, "configs", "private_vars.py")) "Woo! You missed private_vars.py~"
from configs.private_vars import BOT_INFO
from bot_apis import *

# create_automatic_updater() ## probius
create_interactive_updater()  ## maedchen

app = FastAPI(debug=DEBUG)


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
    bot_config = BOT_INFO[is_interactive]
    res = call_messager(
        api_token=bot_config["api_token"],
        chat_id=bot_config["chat_id"],
        message_text=item.text,
        message_link=item.link,
    )
    return res
