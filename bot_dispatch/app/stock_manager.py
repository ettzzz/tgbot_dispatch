#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 15:50:07 2021

@author: eee
"""


import requests

from config.static_vars import DQN_AGENT_HOST


def call_query_status(update, _):
    r = requests.get("{}/api_v1/query_status".format(DQN_AGENT_HOST))
    update.message.reply_text(r.json()["msg"])


def call_reset_status(update, _):
    r = requests.get("{}/api_v1/reset_status".format(DQN_AGENT_HOST))
    update.message.reply_text(r.json()["msg"])
