#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:08:13 2022

@author: eee
"""

import os
import platform

OS = platform.system()
OS_VER = platform.version()
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if "Debian" in OS_VER:
    DEBUG = False
else:
    DEBUG = True
    proxy = 'http://127.0.0.1:8889'
    for k in ["HTTP_PROXY", "HTTPS_PROXY"]:
        os.environ[k] = proxy
        os.environ[k.lower()] = proxy

API_PREFIX = "tgbot"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
BASE_HEADERS = {"User-Agent": UA}
