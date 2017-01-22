# -*- coding:utf-8 -*-
"""
    app/logger.py
    ~~~~~~~~~~~~~~

    应用默认logger定义
"""
import logging
from logging import handlers

__author__ = '"linnchord gao" <linnchord@gmail.com>'

logger = logging.getLogger('app')


def init_logger(log_path=None):
    """
    默认logger初始化
    """
    if not log_path:
        raise RuntimeError(u'No log path defined!')

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

    fh = handlers.WatchedFileHandler(log_path)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
