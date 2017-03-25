# -*- coding:utf-8 -*-
import json
import uuid
from luhu_sharper.flaskapp.kvdb import kvdb
from luhu_sharper.util.transfer import json_dumper_default
import simplejson

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class Payment(object):
    def __init__(self, amount, title, detail, type, user_id=None, object_id=None, callback=None, back_url="",discount_info=None):
        self.amount = amount
        self.user_id = user_id
        self.title = title
        self.detail = detail
        self.type = type
        self.object_id = object_id
        self.discount_info = discount_info
        self.callback = callback


    def save(self):
        key = uuid.uuid4().hex
        dic = dict()
        dic["amount"] = self.amount
        dic["user_id"] = self.user_id
        dic["title"] = self.title
        dic["detail"] = self.detail
        dic["type"] = self.type
        dic["object_id"] = self.object_id
        dic["callback"] = self.callback
        dic["discount_info"] = self.discount_info
        val = simplejson.dumps(dic, use_decimal=True, default=json_dumper_default)
        kvdb.common.set(self.get_full_key(key), val)
        return key

    @classmethod
    def get(cls, key):
        val = kvdb.common.get(cls.get_full_key(key))
        if not val:
            return None
        return json.loads(val)

    @classmethod
    def pop(cls, key):
        val = cls.get(key)
        if val:
            kvdb.common.delete(cls.get_full_key(key))
        return val

    @classmethod
    def get_full_key(cls, key):
        return "pay:obj:%s" % key
