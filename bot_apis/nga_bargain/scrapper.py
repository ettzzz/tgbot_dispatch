#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 14:36:46 2023

@author: eee
"""

import re
import time
import datetime
import random
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


class ngaBargainScrapper:
    def __init__(self):
        seed = random.randint(101, 999)
        self.url = f"https://bbs.nga.cn/read.php?tid=33902411&rand={seed}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
        }
        self._update_cookie()

    def _update_cookie(self):
        _t = round(time.time()) - 60
        self._cookies = {
            "lastvisit": _t,
            "ngaPassportUid": "guest063dc7c568d6cd",
            "bbsmisccookies": {
                "uisetting": {0: "b", 1: 1675394447},
                "pv_count_for_insad": {0: -47, 1: 1675443694},
                "insad_views": {0: 1, 1: 1675443694},
            },
            "guestJs": _t,
        }
        Cookie = "; ".join([f"{k}={quote(str(v))}" for k, v in self._cookies.items()])
        self.headers.update({"Cookie": Cookie})

    def get_raw(self, retry=0):
        if retry >= 3:
            return None
        try:
            r = requests.get(self.url, headers=self.headers)
            if r.status_code != 200:
                return self.get_raw(retry + 1)
            else:
                return r
        except:
            return self.get_raw(retry + 1)

    def data_clean(self, r):
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.select("#postcontent0")
        valid_strs = list()
        if len(tables) < 1:
            return valid_strs

        ts = datetime.datetime.now()
        year = ts.year
        date = datetime.datetime.strftime(ts, "%Y-%m-%d")
        for s in tables[0].contents:
            s = str(s)
            if s.startswith("[color=crimson]"):
                d = re.findall(r"(\d+)月(\d+)日", s)
                if len(d) > 0:
                    _month, _day = d[0]
                    date = f"{year}-{_month.zfill(2)}-{_day.zfill(2)}"
            if s == "<br/>":
                continue
            if "复制" in s and "下单" in s:
                continue
            valid_strs.append(s)

        pair = list()
        for i in range(len(valid_strs) - 1):
            if valid_strs[i + 1].startswith("[url]"):
                title = valid_strs[i].strip()
                link = re.findall(r"\[url\](.*?)\[\/url\]", valid_strs[i + 1])
                link = "" if len(link) == 0 else link[0]
                pair.append((title, link))

        return pair, date


if __name__ == "__main__":
    nga_scrapper = ngaBargainScrapper()
    r = nga_scrapper.get_raw()
    print(r.status_code)
    pair, date = nga_scrapper.data_clean(r)
    print(len(pair))
