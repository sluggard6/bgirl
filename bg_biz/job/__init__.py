# -*- coding:utf-8 -*-
import json
from sharper.flaskapp.kvdb import kvdb
from rq import Queue


__author__ = [
    '"liubo" <liubo@51domi.com>'
]

rqueue = Queue(connection=kvdb.job)  # no args implies the default queue


def write_app_log(data):
    rqueue.enqueue(write_app_log_async, data)


def write_app_log_async(data):
    from luhu_biz.orm.app_log import AppLog

    log = AppLog()
    log.action = data.get('action')
    log.user_id = data.get('user_id')
    log.device_id = data.get('device_id')
    log.key1 = data.get('key1')
    log.key2 = data.get('key2')
    log.key3 = data.get('key3')
    log.data = data.get('data')
    log.ip = data.get('ip')
    if 'create_time' in data:
        log.create_time = data.get('create_time')
    log.insert()

