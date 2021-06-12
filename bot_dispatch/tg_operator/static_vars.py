# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 10:21:43 2021

@author: ert
"""
import os

ROOT = os.getcwd()

ME = '476917241'
ANOTHER_ME = '1433361729'

EMPLOYEE_ROSTER = {
    'probius': {
        'description': 'looking for a rent.',
        'api_token': '781431817:AAEt1G2VaqMyu4OARKLnufp6eqBnHz6zORU',
        'chat_id': ME
        },
    'blog_notify_bot': {
        'description': 'used for ettzzz.me but now it\'s now used for active interactions.',
        'api_token': '966629533:AAFJOn_J_EDEQZPcRftHdSEHHu38PtGxrPI',
        'chat_id': ME
        },
    'jobsuchen_bot': {
        'description': 'looking for a job.',
        'api_token': '764684634:AAHmOxQfMXIHog8q9qaj8Ji2v8SzHJZmt7U',
        'chat_id': ME
        },
    }


UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
BASE_HEADERS = {
    "User-Agent": UA
}

DQN_AGENT_HOST = 'http://82.157.178.246:7704'
