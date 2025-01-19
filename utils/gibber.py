#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 19:59:18 2021

@author: eee
"""

import os
import logging
import logging.config

from configs.static_vars import ROOT, DEBUG


def get_logger(debug=DEBUG):
    """
    # # print log info
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    """

    LOGGING_FMT = "%(asctime)s %(levelname)s %(funcName)s in %(filename)s: %(message)s"
    STREAMING_FMT = "%(levelname)s %(funcName)s %(message)s"
    LOGGING_DATE_FMT = "%Y-%m-%d %a %H:%M:%S"
    LOGGING_NAME = "jibberjabber"

    # create logger
    logger_name = f"{LOGGING_NAME}_logger"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if not debug:
        # create formatter
        formatter = logging.Formatter(LOGGING_FMT, LOGGING_DATE_FMT)
        # create file handler
        log_path = os.path.join(ROOT, f"{LOGGING_NAME}.log")
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        # add handler and formatter to logger
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        formatter = logging.Formatter(STREAMING_FMT, LOGGING_DATE_FMT)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    return logger
