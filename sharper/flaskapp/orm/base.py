# -*- coding:utf-8 -*-
"""
基于SqlAlchemy基础对象
"""
from functools import wraps
import re
import traceback
from flask import flash
from flask_sqlalchemy import SQLAlchemy, Model, declarative_base

from werkzeug.utils import cached_property
from sharper.util import transfer
from sharper.util.string import to_camel_case


__authors__ = ['"linnchord gao" <linnchord@gmail.com>']

db = SQLAlchemy(session_options={'autocommit': True})
# db = SQLAlchemy()
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool


def update_autocommit(dbapi_con, connection_record):
    # 修改autocommit，否则atlas无法实现读写分离
    dbapi_con.autocommit(True)


listen(Pool, 'connect', update_autocommit)


class OrmBase(Model):
    """
    orm基础类
    从flask-sqlalchemy的Model继承以保持BaseModel自定义扩展时语义和db.Model继承一致
    """

    def insert(self):
        self._before_insert()
        db.session.add(self)
        db.session.flush()
        self._after_insert()
        return self

    def update(self):
        self._before_update()
        db.session.merge(self)
        db.session.flush()
        self._after_update()
        return self

    def delete(self):
        self._before_delete()
        db.session.delete(self)
        db.session.flush()
        self._after_delete()


    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def delete_by_id(cls, id):
        obj = cls.get(id)
        if obj: obj.delete()

    def __repr__(self):
        return self.to_json()

    def to_json(self, without=(), include=()):
        return transfer.orm_obj2json(self, without, include)

    def to_dict(self, without=(), include=()):
        return transfer.orm_obj2dict(self, without, include)

    def to_json_dict(self, without=(), include=()):
        return transfer.orm_obj2json_dict(self, without, include)

    @classmethod
    def from_json(cls, json_str):
        return transfer.json2orm_obj(json_str, cls)

    @classmethod
    def from_dic(cls, dic):
        return transfer.dict2obj(dic, cls)

    def _before_insert(self):
        pass

    def _after_insert(self):
        pass

    def _before_update(self):
        pass

    def _after_update(self):
        pass

    def _before_delete(self):
        pass

    def _after_delete(self):
        pass

    def update_json_field(self, field, **kwargs):
        """
        更新某json格式字段内容
        """
        value = getattr(self, field, None)
        if value is None or value.lower() in ["null", "none"]:
            value = {}
        if isinstance(value, (str, unicode)): value = transfer.json2dict(value)
        value.update(**kwargs)
        setattr(self, field, transfer.dict2json(value))

    def replace_json_field(self, field, **kwargs):
        """
        完全替换某json格式字段内容
        """
        setattr(self, field, transfer.dict2json(dict(**kwargs)))

    def get_dict_field(self, field):
        """
        获取json字段的dict表达
        """
        val = getattr(self, field, None) or {}

        if isinstance(val, (str, unicode)):
            r = transfer.json2dict(val)
            return r
        else:
            return val

    def _dict(self, field):
        """
        获取json字段的dict表达 简写
        """
        return self.get_dict_field(field)

    def _clone(self, method='json'):
        """
        复制对象 -用于与db.session分离
        """
        import copy

        if method == 'copy':
            return copy.copy(self)
        elif method == 'json':
            return self.from_json(self.to_json())
        elif method == 'deepcopy':
            return copy.deepcopy(self)
        else:
            return self


    @classmethod
    def _lower_class_name(cls):
        """
        获取类名小写下划线join形式
        """
        return '_'.join(re.findall(r'[A-Z][a-z0-9]*', cls.__name__)).lower()


    @cached_property
    def pk_value(self):
        """
        获取主键字段值 - 只支持单主键
        """
        pk = getattr(self, '_primary_key', None)

        if not pk and hasattr(self, '__table__'):
            for _ in self.__table__.primary_key:
                pk = _.name

        if pk:
            return getattr(self, pk, None)
        else:
            return getattr(self, 'id', None)


    @cached_property
    def all_data_field(self):
        """
        获取对象自身所有数据表映射字段名
        """
        return self.load_all_data_field()

    @classmethod
    def load_all_data_field(cls):
        """
        获取类自身所有数据表映射字段名
        """
        if hasattr(cls, '__table__'):
            return [c.name for c in cls.__table__.columns]

    def try_to_add_ip(self):
        ip_column = 'ip'
        # 检查是否有ip这个field，如果有并且没有值，则从flask request对象里面取
        if ip_column in self.load_all_data_field():
            ip_val = getattr(self, ip_column)
            if not ip_val:
                from flask import request

                setattr(self, ip_column, request.headers.get('X-Forwarded-For', None) or request.remote_addr)

    def try_to_add_device_info(self):
        device_infos = ['imei', 'mac']
        # 检查是否有ip这个field，如果有并且没有值，则从flask request对象里面取
        for info in device_infos:
            if info in self.load_all_data_field():
                info_val = getattr(self, info)
                if not info_val:
                    from flask import request

                    info_val = request.args.get(info, "")
                    if info_val:
                        setattr(self, info, info_val)

    def save(self):
        if self.id:
            self.update()
        else:
            self.insert()


            # def __getattr__(self, name):
            # if name[-3:] == "_cn":
            # attr_name = name[:-3]
            # clz_name = to_camel_case(attr_name)
            # try:
            # clz = getattr(self, clz_name)
            # if clz:
            # return clz().get_display_cn(getattr(self, attr_name))
            # except Exception:
            # raise Exception("%s undefined" % clz_name)
            #


def init_base(cls):
    """
    orm base custom
    """

    # 保持原db.Model语义
    # copy from flask.ext.sqlalchemy
    # db.Model = SQLAlchemy.make_declarative_base
    import flask_sqlalchemy as sqla

    base = declarative_base(cls=cls, name='Model', metaclass=sqla._BoundDeclarativeMeta)

    base.query = sqla._QueryProperty(db)

    # 扩展初始化方法代码
    def _init(self, *args, **kargs):
        """
        自定义orm对象初始化方法， 传入参数顺序需和对象字段声明顺序保持一致
        """
        if hasattr(self, '__table__'):
            orm_attr_list = [c.name for c in self.__table__.columns if not (
                c.primary_key and c.autoincrement)]
            if args:
                for i in xrange(len(args)):
                    setattr(self, orm_attr_list[i], args[i])
            if kargs:
                for attr in orm_attr_list[len(args):]:
                    setattr(self, attr, kargs.get(attr))

    base.__init__ = _init

    return base


BaseModel = init_base(OrmBase)


def dict2json(target, value, oldvalue, initiator):
    """
    用于sqlalchemy对象设置属性时参数转换

    示例: post.py
    from sqlalchemy import event
    event.listen(Post.content, 'set', dict2json, retval=True)
    """
    return transfer.dict2json(value)


def transaction(f):
    @wraps(f)
    def do(*args, **kwargs):
        # flush_method = db.session.flush
        # commit_method = db.session.commit
        try:
            # db.session.commit = flush_method
            db.engine.execute("set autocommit=0")
            db.session.begin(subtransactions=True)
            ret = f(*args, **kwargs)
            # db.session.commit = commit_method
            db.session.commit()
            return ret
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            raise e
        finally:
            db.engine.execute("set autocommit=1")
            # db.session.commit = commit_method

    return do


def transaction_for_apk(f):
    @wraps(f)
    def do(*args, **kwargs):
        flush_method = db.session.flush
        commit_method = db.session.commit
        try:
            db.session.begin()
            db.session.commit = flush_method
            ret = f(*args, **kwargs)
            db.session.commit = commit_method
            db.session.commit()
            return ret
        except Exception as e:
            # print e
            db.session.rollback()
            import traceback
            # traceback.print_exc()
            flash(u'添加APK失败', 'fail')
        finally:
            db.session.commit = commit_method

    return do