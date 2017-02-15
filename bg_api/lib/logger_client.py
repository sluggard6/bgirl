# -*- coding: utf-8 -*-
import logging
from logging import handlers

logger_client = logging.getLogger('client')
logger_pay = logging.getLogger('pay')


def init_logger_client(app):
    file_name = app.config.get('APP_LOG_CLIENT_FILE', '/var/log/bgirl/%s_client.log' % app.name)

    logger_client.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

    fh = handlers.WatchedFileHandler(file_name)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger_client.addHandler(fh)


def init_pay_logger_client(app):
    file_name = app.config.get('APP_LOG_CLIENT_PAY_FILE', '/var/log/bgirl/pay.log')

    logger_pay.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

    fh = handlers.WatchedFileHandler(file_name)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger_pay.addHandler(fh)