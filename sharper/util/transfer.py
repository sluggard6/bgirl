# -*- coding:utf-8 -*-
"""
    util/format.py
    ~~~~~~~~~~~~~~

    simple format tools

    :author: linnchord@gmail.com
    :date:2011-10-09

"""

from datetime import date, datetime
from decimal import Decimal
import simplejson as json
import sqlalchemy
from .helper import get_datetime, get_float, get_int, get_utf8, get_unicode, get_str


def json_dumper_default(obj):
    """
    json.dumps(dict, default=util.format.json_dumper_default)
    json dumps 提供默认转换方法，对datetime字段做特别处理
    """

    if obj:
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            TWOPLACES = Decimal(10) ** -2
            obj.quantize(TWOPLACES)
            return str(obj)
        else:
            raise TypeError('%r is not JSON serializable' % obj)
    else:
        return obj


def json2orm_obj(json_text, cls):
    """
    json转换至sqlalchemy对象
    """
    return dict2orm_obj(json.loads(json_text), cls)


def dict2orm_obj(dic, cls):
    """
    dict转换至sqlalchemy对象，针对DateTime类型处理
    """
    obj = cls()
    for d in dic:
        value = dic[d]
        if value \
                and (cls.__table__.columns.get(d) is not None) \
                and isinstance(cls.__table__.columns[d].type, sqlalchemy.types.DateTime):
            value = get_datetime(value)
        setattr(obj, d, value)
    return obj


def orm_obj2json(obj, without=(), include=()):
    """
    将sqlalchemy对象转换为json
    """
    return dict2json(orm_obj2dict(obj, without, include))


def orm_obj2dict(obj, without=(), include=()):
    """
    将sqlalchemy对象转换为dict - 仅转换对应数据表字段
    """
    dic = {}
    for c in obj.__table__.columns:
        if c.name not in without and (c.name in include if include else True):
            dic[c.name] = getattr(obj, c.name)
    return dic


def orm_obj2json_dict(obj, without=(), include=()):
    """
    将sqlalchemy对象转换为dict - 特别处理DateTime
    """
    dic = {}
    for c in obj.__table__.columns:
        if c.name not in without and (c.name in include if include else True):
            value = getattr(obj, c.name)
            if value and isinstance(c.type, sqlalchemy.types.DateTime):
                dic[c.name] = strftime(value)
            else:
                dic[c.name] = value
    return dic


def obj2dict(obj, attrs=None):
    """
    普通对象转换为dict

    @attrs: 指定转换字段，未指定则直接获取__dict__ ('name', 'sex', 'age')
    """
    dic = {}
    if attrs:
        for attr in attrs:
            try:
                dic[attr] = getattr(obj, attr)
            except AttributeError:
                pass
        return dic
    else:
        return obj.__dict__


def obj2json(obj, attrs=None):
    return dict2json(obj2dict(obj, attrs))


def json2obj(json_text, cls):
    """
    json转换至对象
    """
    return dict2obj(json.loads(json_text), cls)


def dict2obj(dic, cls):
    """
    dict转换至对象，针对DateTime类型自定义Time结尾命名变量处理
    """
    obj = cls()
    for d in dic:
        value = dic[d]
        if d.lower().endswith(('time', '_at')): value = get_datetime(value)
        setattr(obj, d, value)
    return obj


def dict2json(dic):
    """
    将dict对象转换为json
    """
    if isinstance(dic, basestring):
        return dic
    return json.dumps(dic, use_decimal=True, default=json_dumper_default, ensure_ascii=False)


dict2str = dict2json


def json2dict(_str):
    """json字符串转换为dict"""
    dic = json.loads(_str) if isinstance(_str, basestring) else _str
    if isinstance(dic, dict):
        for d in dic:
            if d.lower().endswith(('time', '_at')):
                dic[d] = get_datetime(dic[d])
    return dic


str2dict = json2dict


def dbrow2obj(row, cls):
    if row:
        obj = cls()
        for c in obj.__table__.columns:
            setattr(obj, c.name, row[c])
        return obj
    return None


def dbrow2dict_obj(row):
    from luhu_sharper.lib.dict_proxy import DictProxyObject

    obj = DictProxyObject()
    if row:
        obj = DictProxyObject()
        for k, v in row.items():
            obj[k] = v
    return obj


def dbrows2dict_obj_list(rows):
    return [dbrow2dict_obj(row) for row in rows]


def strftime(date, default=None, fmt='%Y-%m-%d %H:%M:%S'):
    if date:
        return datetime.strftime(date, fmt)
    else:
        return default


def strptime(date_str, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(date_str, fmt)


type_get_func_map = dict(
    int=get_int, float=get_float, datetime=get_datetime, date=get_datetime, str=get_str
)


def dict2vars(dic, var_name_list):
    """
    根据键列表从字典获取值列表
    通常用于变量批量赋值

    可定义变量类型 支持类型参考 type_get_func_map

    例：user_name, sex, age = dict2vars(request.get_json(), ('str:user_name', 'int:sex', 'int:age'))
    """
    if isinstance(var_name_list, basestring):
        var_name_list = [var_name_list]
    ret = []
    for var in var_name_list:
        if ':' in var:
            typ, var_name = var.split(':')
            func = type_get_func_map.get(typ, lambda x: x)
            ret.append(func(dic.get(var_name)))
        else:
            ret.append(dic.get(var))
    return ret


def dict2orm(dic, cls_obj, include=(), out=(), mapper={}):
    """
    将字典赋值到对象（传入类则生成对象）

    cls_obj必须为BaseModel子类或对象

    @dic: 字典数据
    @cls_obj: 对象或类
    @include: 包含字段属性
    @out: 不包含字段属性
    @mapper: 字典到对象属性非同名时映射 dict(user_name='name', age='old')
    """
    import inspect

    if inspect.isclass(cls_obj):
        cls_obj = cls_obj()

    if not include:
        include = cls_obj.all_data_field
    if out:
        include = set(include) - set(out)

    for attr in include:
        if hasattr(cls_obj, attr) and attr in dic:
            setattr(cls_obj, attr, dic.get(attr))

    for k, v in mapper.items():
        setattr(cls_obj, v, dic.get(k))

    return cls_obj


