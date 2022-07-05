#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 11:06:47 2022

@author: eee
"""

import time
import datetime

DATE_FORMAT = "%Y-%m-%d"


def struct_timestr(timestr, _format=DATE_FORMAT):
    structed_time = time.strptime(timestr, _format)
    return structed_time


def struct_datestr(datestr, _format=DATE_FORMAT):
    structed_date = datetime.datetime.strptime(datestr, _format)
    return structed_date


def get_now():
    return time.time()


def get_today_date():
    today = datetime.datetime.now()
    today_str = datetime.datetime.strftime(today, DATE_FORMAT)
    return today_str


def get_delta_date(date, days):
    # type(date) is str
    strd = struct_datestr(date)
    target_strd = strd + datetime.timedelta(days)
    target_datestr = datetime.datetime.strftime(target_strd, DATE_FORMAT)
    return target_datestr  # type(target_datestr) is str
