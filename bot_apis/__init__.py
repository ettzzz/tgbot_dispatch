#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:10:28 2022

@author: eee
"""


from .helloworld.test import test_hello_world
from .send_message.messager import call_messager
from .v2ray_update.nice_scrapper import call_get_latest_v2ray_file
from .v2ray_update.nice_scrapper import call_nice_scrapper
from .flight_discount.flight_reminder import call_flight_reminder

from ._manager import create_automatic_updater, create_interactive_updater

__all__ = [
    "create_automatic_updater",
    "create_interactive_updater",
    "test_hello_world",
    "call_messager",
    "call_get_latest_v2ray_file",
    "call_nice_scrapper",
    "call_flight_reminder",
]
