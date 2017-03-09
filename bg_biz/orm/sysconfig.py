# -*- coding: utf-8 -*-
"""
系统配置表

存储各类系统设置变量
"""
import json
from sharper.flaskapp.kvdb import kvdb
from sharper.flaskapp.orm.base import BaseModel, db


class SysConfig(BaseModel):
    __tablename__ = 'sys_config'

    _kvdb_key = 'g:sysconfig'

    name = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    descr = db.Column(db.String(2000), nullable=False)

    def __init__(self, name=None, value=None, descr=None):
        self.name = name
        self.value = value
        self.descr = descr


    def _after_insert(self):
        kvdb.common.hset(self._kvdb_key, self.name, self.value)

    _after_update = _after_insert


    def _after_delete(self):
        kvdb.common.hdel(self._kvdb_key, self.name)

    @classmethod
    def get(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_config(cls, key):
        value = kvdb.common.hget(cls._kvdb_key, key)

        if not value:
            if not kvdb.common.exists(cls._kvdb_key):
                cls.refresh_kvdb()
                value = kvdb.common.hget(cls._kvdb_key, key)

        return value or ''

    @classmethod
    def get_json(cls, key):
        val = cls.get_config(key)
        if val:
            return json.loads(val)
        return None

    @classmethod
    def clear_kvdb(cls):
        kvdb.common.delete(cls._kvdb_key)


    @classmethod
    def refresh_kvdb(cls):
        cls.clear_kvdb()
        for conf in cls.query.all():
            kvdb.common.hset(cls._kvdb_key, conf.name, conf.value)

