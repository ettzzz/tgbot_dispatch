#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:22:42 2022

@author: eee
"""

from utils.datetime_tools import get_today_date, get_delta_date, struct_datestr


class _flightDiscountCheckup:
    def __init__(self, today):

        self.dates = []
        for i in range(1, 7):
            self.dates.append(get_delta_date(today, i))
        self.timetable = self._init_timetable()

    def _init_timetable(self):
        """
        keywords: month, date, day, hour. All in int
        day means week day index, starting from 0, means Monday
        updated on 20220902
        """
        timetable = {
            "国航": {"if": "month==date"},
            "南方航空": {"if": "date==28"},
            "东方航空": {"if": "date==18"},
            "中国联合航空": {"if": "day==4"},
            "四川航空": {"if": "date==19"},
            "春秋航空": {"if": "date in [9, 15, 27]"},
            "厦门航空": {"if": "date==9"},
            "吉祥航空": {"if": "date==25"},
            "西部航空": {"if": "day==2"},
            "昆明航空": {"if": "date==16"},
            "深圳航空": {"if": "date==12"},
        }
        return timetable

    def check(self):
        result = dict()

        for datestr in self.dates:
            result[datestr] = list()
            sdate = struct_datestr(datestr)
            month = sdate.month
            date = sdate.day
            day = sdate.weekday()
            for flight_org, cond in self.timetable.items():
                if eval(cond["if"]) is True:
                    result[datestr].append(flight_org)

        return result


def call_flight_reminder():
    today = get_today_date()
    inspector = _flightDiscountCheckup(today)
    result = inspector.check()
    text = ""
    for datestr, orgs in result.items():
        if orgs:
            text += f"{datestr}优惠航司有：{','.join(orgs)}。\n"
    if len(text) == 0:
        text = f"未来{len(result)}天没有优惠哦。"

    return text
