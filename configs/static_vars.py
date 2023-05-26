#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:08:13 2022

@author: eee
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEBUG = os.getenv("DEBUG") != "0"
if DEBUG:
    proxy = 'http://127.0.0.1:8889'
    for k in ["HTTP_PROXY", "HTTPS_PROXY"]:
        os.environ[k] = proxy
        os.environ[k.lower()] = proxy

_CHAT_ID = os.getenv("TG_CHAT_ID")
_MAEDCHENAI_TOKEN = os.getenv("MAI_TOKEN")
_PROBIUS_TOKEN = os.getenv("PROBIUS_TOKEN")
BOT_INFO = {
    0: {
        "name": "probius",
        "description": "A bot for all automatic notifications.",
        "api_token": _PROBIUS_TOKEN,
        "chat_id": _CHAT_ID,
    },
    1: {
        "name": "maedchenai",
        "description": "A bot for all interactive notifications.",
        "api_token": _MAEDCHENAI_TOKEN,
        "chat_id": _CHAT_ID,
    },
}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
BASE_HEADERS = {"User-Agent": UA}
