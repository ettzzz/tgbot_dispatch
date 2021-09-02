# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 10:21:43 2021

@author: ert
"""

import os

from private.private_info import EMPLOYEE_ROSTER, DQN_AGENT_HOST
from private.private_info import pois

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
BASE_HEADERS = {
    "User-Agent": UA
}
