# -*- coding:utf-8 -*-
"""
    util/helper.py
    ~~~~~~~~~~~~~~

    simple helper tools

    :author: linnchord@gmail.com
    :date:2011-07-21

"""
import random
import re
from datetime import datetime, date, time, timedelta
from flask import request


def good_cache_time(age='m', offset=0.3):
    """
    产生抖动缓存时间(秒)，防止缓存集中刷新

    @age: 时间参数
        m/月, 1d/天, 2h/小时 M/分钟 s/秒 省略数字则默认为1 传入int则为秒
        秒抖动较小，忽略抖动
        默认30%差异抖动 可传入offset自定义(0-1小数)
    """
    if isinstance(age, int):
        count, unit = age, 's'
    elif len(age) == 1:
        count, unit = '1', age
    else:
        count, unit = age[0:-1], age[-1]

    if unit not in 'Mmdhs' or not count.isdigit() or offset > 1 or offset < 0:
        raise RuntimeError(u'抖动缓存时间获取参数格式错误')

    if unit == 'm':
        count = int(count) * 3600 * 24 * 30
    elif unit == 'd':
        count = int(count) * 3600 * 24
    elif unit == 'h':
        count = int(count) * 3600
    elif unit == 'M':
        count = int(count) * 60
    elif unit == 's':
        count = int(count)

    return random.randint(int(count * (1 - offset)), int(count * (1 + offset)))


def random_sample(lst, limit=1):
    """
    从一个集合中随机抽取n个
    """
    if len(lst) > limit:
        return random.sample(lst, limit)
    else:
        return lst


def is_number(s):
    try:
        n = str(float(s))
        if n == "nan" or n == "inf" or n == "-inf":
            return False
    except ValueError:
        try:
            complex(s)  # for complex
        except ValueError:
            return False
    return True


def is_int(s):
    try:
        n = str(int(s))
        if n == "nan" or n == "inf" or n == "-inf":
            return False
    except ValueError:
        return False
    return True


def swap_dict_key_value(obj):
    """
    交换dict结构的key/value 支持dict类型和[(key, value)..]格式list
    @param obj:
    @return:
    """
    new = None
    if isinstance(obj, dict):
        new = {}
        for d in obj:
            new[obj[d]] = d
    elif isinstance(obj, list):
        new = []
        for l in obj:
            new.append((l[1], l[0]))
    return new


def get_datetime(obj, default=None, fmt=None):
    """
    从文本获取日期时间 无法转换返回None
    可识别 %Y-%m-%d %H:%M:%S / %Y-%m-%d %H:%M / %Y-%m-%d 或其他自定义格式

    @obj: 待转换文本/timestamp
    @default: 默认值
    @fmt: 指定格式
    """
    if isinstance(obj, basestring):
        try:
            obj = obj.strip()
            if fmt:
                obj = datetime.strptime(obj, fmt)
            else:
                if ' ' in obj:
                    if len(obj.split(':')) > 2:
                        obj = datetime.strptime(obj, '%Y-%m-%d %H:%M:%S')
                    else:
                        obj = datetime.strptime(obj, '%Y-%m-%d %H:%M')
                else:
                    obj = datetime.strptime(obj, '%Y-%m-%d')
        except:
            pass
    return obj if isinstance(obj, datetime) else default


def get_int(obj, default=None):
    if not obj:
        return default
    try:
        return int(obj)
    except:
        return default


def get_float(obj, default=None):
    if not obj:
        return default
    try:
        return float(obj)
    except:
        return default


def get_utf8(_, from_code='utf8'):
    """
    获取utf8编码字符串 无效返回原字符串
    """
    _ = get_str(_)
    if isinstance(_, unicode):
        return _.encode('utf8')
    if isinstance(_, str):
        if from_code in ('utf8', 'utf-8'):
            return _
        else:
            try:
                return _.decode(from_code).encode('utf8')
            except:
                return _
    return _


def get_unicode(_, from_code='utf8'):
    """
    获取unicode字符串 无效返回None
    """
    _ = get_str(_)
    if isinstance(_, unicode):
        return _
    if isinstance(_, str):
        try:
            return _.decode(from_code)
        except:
            pass

    return None


def get_str(_, default=None):
    try:
        if _:
            return str(_).strip()
        else:
            return default
    except:
        return default


def get_dict_val(keys, dic, spliter='.'):
    """
    获取dict多层值

    get_dict_val('a.b.c', {'a':{'b':{'c':123}}})
    """
    if spliter in keys:
        tmp = keys.split(spliter)
        cur = dic.get(tmp[0])
        if isinstance(cur, dict):
            return get_dict_val(spliter.join(tmp[1:]), cur, spliter)
        else:
            return None
    else:
        return dic.get(keys)


def is_mobile():
    user_agent = request.headers.get('User-Agent')
    return user_agent and (
        re.search('iPod|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP|IEMobile', user_agent))


def is_pad():
    user_agent = request.headers.get('User-Agent')
    return user_agent and (
        re.search('iPad', user_agent))


def get_time_pass_text(date_time, three_day_before_format='%y-%m-%d %H:%M'):
    """
    根据时间获取距当前时间差的文本描述, three_day_before_format为三天之前的时间格式
    """
    if isinstance(date_time, (str, unicode)):
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    today_start = datetime.combine(date.today(), time())
    pass3day_start = datetime.combine(date.today() - timedelta(days=3), time())

    day1 = 3600 * 24
    hour1 = 3600
    mi1 = 60

    if date_time < pass3day_start:
        return date_time.strftime(three_day_before_format)

    if date_time < today_start:
        _pas = int((today_start - date_time).total_seconds())
        return u'%s天前' % (_pas / day1 + 1)

    pas = int((datetime.now() - date_time).total_seconds())

    if pas >= hour1: return u'%s小时前' % (pas / hour1)
    if pas >= mi1: return u'%s分钟前' % (pas / mi1)
    if pas < 0: pas = 0
    return u'%s秒前' % pas
