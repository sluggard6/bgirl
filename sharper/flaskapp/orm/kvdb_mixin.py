# -*- coding:utf-8 -*-
"""
    针对SqlAlchemy基础对象实现kvdb mixin
"""
import pickle

from sqlalchemy.orm.exc import NoResultFound

from ..kvdb import kvdb
from luhu_sharper.lib.error import AppError
from luhu_sharper.util import helper
from luhu_sharper.lib.validator import is_numeric


__authors__ = ['"linnchord gao" <linnchord@gmail.com>']


class KvdbMixin(object):
    """
    对BaseModel提供kvdb缓存相关功能
    """

    # 缓存kvdb引用，继承后请自定义
    kvdb = kvdb.common

    # 缓存时间，若不设置则获取 helper.good_cache_time()
    _primary_cache_time = None
    #缓存关键名，若不设置则获取类名小写 cls.__name__.lower()
    _primary_cache_name = None

    @classmethod
    def get_by_kvdb(cls, id):
        _key = cls._primary_kvdb_key(id)
        r = cls.kvdb.get(_key)
        if r:
            # print "get: %s" % _key
            return cls.from_json(r)
        else:
            r = cls.query.get(id)
            if r:
                cls.kvdb.setex(_key, r.to_json(), cls._primary_cache_time or helper.good_cache_time())
                return r
        return None

    def set_by_kvdb(self):
        pk_value = getattr(self, 'pk_value', None)
        if not pk_value: raise AppError(u'Get None of PrimaryKey value when find in KvdbMixin with OrmBase!')
        _key = self._primary_kvdb_key(pk_value)
        self.kvdb.setex(_key, self.to_json(), self._primary_cache_time or helper.good_cache_time())

    def get_kvdb_ex(self, ex):
        _key = self._build_kvdb_key(ex, self.id)
        return self.kvdb.get(_key)

    def set_kvdb_ex(self, ex, value):
        _key = self._build_kvdb_key(ex, self.id)
        self.kvdb.setex(_key, value, self._primary_cache_time or helper.good_cache_time())

    @classmethod
    def get_by_kvdb_unique(cls, idx, val):
        _key = cls._build_kvdb_key(idx, val)
        r = cls.kvdb.get(_key)
        if r:
            return cls.from_json(r)
        else:
            if is_numeric(val):
                sql = '%s=%s' % (idx, val)
            else:
                sql = "%s='%s'" % (idx, val)
            #try:
            r = cls.query.filter(sql).first()
            #except NoResultFound:
            #    return None
            if r:
                cls.kvdb.setex(_key, r.to_json(), cls._primary_cache_time or helper.good_cache_time())
                return r
            else:
                print "cache and db get None:",_key
        return None

    @classmethod
    def _primary_kvdb_key(cls, *args, **kargs):
        """
        build primary kvdb key
        """
        return cls._build_kvdb_key('primary', *args, **kargs)

    @classmethod
    def _build_kvdb_key(cls, type, *args, **kargs):
        """
        build kvdb_key
        """
        k = cls._primary_cache_name or cls.__name__.lower()
        if type != 'primary': k += ':' + type
        if args:
            k += ':' + ':'.join([str(arg) for arg in args])
        if kargs:
            for karg in kargs:
                k += ':%s:%s' % (karg, kargs[karg])
        return k

    def clear_primary_kvdb(self):
        """清除主键对象缓存"""
        from luhu_sharper.lib.error import AppError

        pk_value = getattr(self, 'pk_value', None)
        if not pk_value: raise AppError(u'Get None of PrimaryKey value when find in KvdbMixin with OrmBase!')
        self.kvdb.delete(self._primary_kvdb_key(pk_value))

    def clear_unique_kvdb(self, idx, val):
        """清除唯一键对象缓存"""
        self.kvdb.delete(self._build_kvdb_key(idx, val))


class KvdbMixinPickle(object):
    """
    对BaseModel提供kvdb缓存相关功能
    """

    # 缓存kvdb引用，继承后请自定义
    kvdb = kvdb.common

    # 缓存时间，若不设置则获取 helper.good_cache_time()
    _primary_cache_time = None
    #缓存关键名，若不设置则获取类名小写 cls.__name__.lower()
    _primary_cache_name = None

    @classmethod
    def get_by_kvdb(cls, id):
        _key = cls._primary_kvdb_key(id)
        r = cls.kvdb.get(_key)
        if r:
            return pickle.loads(r)
        else:
            r = cls.query.get(id)
            if r:
                cls.kvdb.setex(_key, pickle.dumps(r), cls._primary_cache_time or helper.good_cache_time())
                return r
        return None

    @classmethod
    def _primary_kvdb_key(cls, *args, **kargs):
        """
        build primary kvdb key
        """
        return cls._build_kvdb_key('primary', *args, **kargs)

    @classmethod
    def _build_kvdb_key(cls, type, *args, **kargs):
        """
        build kvdb_key
        """
        k = cls._primary_cache_name or cls.__name__.lower()
        if type != 'primary': k += ':' + type
        if args:
            k += ':' + ':'.join([str(arg) for arg in args])
        if kargs:
            for karg in kargs:
                k += ':%s:%s' % (karg, kargs[karg])

        return k


    def clear_primary_kvdb(self):
        pk_value = getattr(self, 'pk_value', None)
        if not pk_value: raise AppError(u'Get None of PrimaryKey value when find in KvdbMixinPickle with OrmBase!')
        self.kvdb.delete(self._primary_kvdb_key(pk_value))

