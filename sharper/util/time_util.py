# -*- coding:utf-8 -*-
"""
    domi/util/time.py
    ~~~~~~~~~~~~~~

    时间类工具方法
"""
from datetime import datetime, date, time, timedelta
from .helper import get_datetime

__authors__ = ['"linnchord gao" <linnchord@gmail.com>']


def get_time_pass_text(date_time, three_day_before_format='%y-%m-%d %H:%M'):
    """
    根据时间获取距当前时间差的文本描述, three_day_before_format为三天之前的时间格式
    """
    if isinstance(date_time, basestring):
        date_time = get_datetime(date_time)

    if isinstance(date_time, int):
        date_time = datetime.fromtimestamp(date_time)

    if not isinstance(date_time, datetime):
        raise RuntimeError(u'Para date_time must be datetime format text or timestamp or datetime object!')

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


def chinese_zodiac(*args):
    """
    获取生肖

    可传参数
    @dateortime datetime或date类型

    或
    @year int
    @month int
    @day int
    """
    year = month = day = 0
    if len(args) == 1:
        if isinstance(args[0], (datetime, date)):
            year, month, day = args[0].year, args[0].month, args[0].day
    if len(args) == 3:
        year, month, day = args
    if not (year and month and day):
        return None

    from lunardate import LunarDate

    return u'猴鸡狗猪鼠牛虎兔龙蛇马羊'[LunarDate.fromSolarDate(year, month, day).year % 12]


def zodiac(*args):
    """
    获取星座

    可传参数
    @dateortime datetime或date类型

    或
    @year int
    @month int
    """
    month = day = 0
    if len(args) == 1:
        if isinstance(args[0], (datetime, date)):
            month, day = args[0].month, args[0].day
    if len(args) == 2:
        month, day = args

    if not (day and month):
        return None

    return get_constellation(month, day)


def get_constellation(month, day):
    """获取对应的星座"""
    #魔羯座 ( 12/22 - 01/19 )	 水瓶座 ( 01/ 20- 02/18 )	 双鱼座 ( 02/19- 03/20 )	 白羊座 ( 03/21 - 04/20 )
    #金牛座 ( 04/21 - 05/20 )	 双子座 ( 05/21 - 06/21 )	 巨蟹座 ( 06/22- 07/22 )	 狮子座 ( 07/23 - 08/22 )
    #处女座 ( 08/23 - 09/22 )	 天秤座 ( 09/23 - 10/23 )	 天蝎座 ( 10/24 - 11/22 )	 射手座 ( 11/23 - 12/21 )
    dates = (20, 19, 21, 21, 21, 22, 23, 23, 23, 24, 23, 22)
    constellations = (u"摩羯", u"水瓶", u"双鱼", u"白羊", u"金牛", u"双子", u"巨蟹",
                      u"狮子", u"处女", u"天秤", u"天蝎", u"射手", u"摩羯")
    if day < dates[month - 1]:
        return constellations[month - 1]
    else:
        return constellations[month]


'''
'76', '新年'
'78', '情人节'
'80', '女人节'
'81', '白色情人节'
'82', '愚人节'
'83', '劳动节'
'85', '520节'
'86', '儿童节'
'89', '教师节'
'91', '国庆节'
'93', '万圣节'
'94', '光棍节'
'96', '圣诞节'
'''
'''
新年(元旦)	1月1日
情人节(214)	2月14日
女人节	3月8日
白色情人节	3月14日
愚人节	4月1日
劳动节	5月1日
520节	5月20日
儿童节	6月1日
教师节	9月1日
国庆节	10月1日
万圣节	11月1日
光棍节	11月11日
圣诞节	12月25日
'''
__solar_festivals__ = {
    1301: {
        "index_id": 76,
        "name": u"新年"
    },
    101: {
        "index_id": 76,
        "name": u"新年"
    },
    214: {
        "index_id": 78,
        "name": u"情人节"
    },
    308: {
        "index_id": 80,
        "name": u"白色情人节"
    },
    314: {
        "index_id": 81,
        "name": u"白色情人节"
    },
    401: {
        "index_id": 82,
        "name": u"愚人节"
    },
    501: {
        "index_id": 83,
        "name": u"劳动节"
    },
    520: {
        "index_id": 85,
        "name": u"520节"
    },
    601: {
        "index_id": 86,
        "name": u"儿童节"
    },
    910: {
        "index_id": 89,
        "name": u"教师节"
    },
    1001: {
        "index_id": 91,
        "name": u"国庆节"
    },
    1101: {
        "index_id": 93,
        "name": u"万圣节"
    },
    1111: {
        "index_id": 94,
        "name": u"光棍节"
    },
    1225: {
        "index_id": 96,
        "name": u"圣诞节"
    }
}

'''
'77', '中国新年' 中国新年	农历正月初一
'79', '元宵节' 元宵节	农历正月15
'88', '端午节' 端午节	农历5月初5
'90', '中秋节' 中秋节	农历8月15
'92', '重阳节' 重阳节	农历9月初9
'''
__lunar_festival__ = {
    1301: {
        "index_id": 77,
        "name": u"中国新年"
    },
    1315: {
        "index_id": 79,
        "name": u"元宵节"
    },
    101: {
        "index_id": 77,
        "name": u"中国新年"
    },
    115: {
        "index_id": 79,
        "name": u"元宵节"
    },
    505: {
        "index_id": 88,
        "name": u"端午节"
    },
    815: {
        "index_id": 90,
        "name": u"中秋节"
    },
    909: {
        "index_id": 92,
        "name": u"重阳节"
    }
}

'''
'84', '母亲节'  母亲节	5月第二个星期日
'87', '父亲节' 父亲节	6月第3个星期日
'95', '感恩节' 感恩节	11月第4个星期四
id为月份/星期/星期几（0为周一）
'''

__week_festival__ = {
    "5-2-6": {
        "index_id": 84,
        "name": u"母亲节"
    },
    "6-3-6": {
        "index_id": 87,
        "name": u"父亲节"
    },
    "11-4-3": {
        "index_id": 95,
        "name": u"感恩节"
    }
}


def convert_week_festival(year, month, week, weekday):
    '''
    将第几周星期几这种类型的节日转换成对应的日期
    '''
    first_day = datetime.strptime("%s-%s-01" % (year, month), "%Y-%m-%d")
    first_weekday = first_day.weekday()
    if first_weekday <= weekday:
        return first_day + timedelta(days=7 * (week - 1) + weekday - first_weekday)
    else:
        return first_day + timedelta(days=7 * week + weekday - first_weekday)


WEEK_SECONDS = 7 * 24 * 3600


def weeks_after(start, now):
    start_seconds = int(start.strftime("%s"))
    now_seconds = int(now.strftime("%s"))
    if start_seconds > now_seconds:
        return 0
    duration = (now_seconds - start_seconds)
    return duration / WEEK_SECONDS + 1

def days_after(start, now):
    start_seconds = int(start.strftime("%s"))
    now_seconds = int(now.strftime("%s"))
    if start_seconds > now_seconds:
        return 0
    duration = (now_seconds - start_seconds)
    return duration / WEEK_SECONDS + 1
