#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:42:14 2022

@author: eee
"""

import requests

from configs.static_vars import UA


def call_messager(api_token, chat_id, message_text, message_link=""):
    """
    Parameters
    ----------
    api_token : STR
        len = 45
    chat_id : STR
        len = 9.
    message_text : STR
        anything you want.
    message_link : STR, optional
        valid http link. The default is "".

    Returns
    -------
    INT
        status code from telegram bot website.

    """
    base_url = f"https://api.telegram.org/bot{api_token}/sendMessage"
    html_text = f'<a href="{message_link}">{message_text}</a>'
    params = {
        "chat_id": chat_id,
        "text": html_text,
        "disable_web_page_preview": "True",
        "parse_mode": "HTML",
    }
    try:
        r = requests.get(
            url=base_url, params=params, headers={"User-Agent": UA}, timeout=5
        )
    except:
        # TODO: logger?
        return {"msg": 0}  ## timeout or something else

    return {"msg": r.status_code}
