# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 10:22:17 2021

@author: ert
"""

import requests

from .static_vars import UA, EMPLOYEE_ROSTER


def send_message(to, message_link, message_text):
    if to in EMPLOYEE_ROSTER:
        chat_id = EMPLOYEE_ROSTER[to]['chat_id']
        token = EMPLOYEE_ROSTER[to]['api_token']
    else:
        return -1
        
    base_url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    html_text = '<a href="{}">{}</a>'.format(message_link, message_text)
    params = {
        'chat_id': chat_id,
        'text': html_text,
        'disable_web_page_preview': 'True',
        'parse_mode': 'HTML'
        }
    
    r = requests.get(
        base_url,
        params = params,
        headers = {'User-Agent': UA},
        timeout = 10
        )
    
    return r.status_code


