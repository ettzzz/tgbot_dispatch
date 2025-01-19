#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:08:13 2022

@author: eee
"""

import os


ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEBUG = os.getenv("DEBUG") != "0"
