# -*- coding:utf-8 -*-
from calendar import monthrange
from datetime import datetime, timedelta

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


def get_first_time_of_month(year=None, month=None):
    if not year or not month:
        now = datetime.now()
        if not year:
            year = now.year
        if not month:
            month = now.month
    return datetime(year, month, 1, hour=0, minute=0, second=0)


def get_last_time_of_month(year=None, month=None):
    if not year or not month:
        now = datetime.now()
        if not year:
            year = now.year
        if not month:
            month = now.month
    first_day, last_day = monthrange(year, month)
    return datetime(year, month, last_day, hour=23, minute=59, second=59)


def get_tomorrow(year=None, month=None, day=None):
    if not year or not month or not day:
        now = datetime.now()
        if not year:
            year = now.year
        if not month:
            month = now.month
        if not day:
            day = now.day
    return datetime(year, month, day) + timedelta(days=1)


def is_same_day(date1, date2):
    if date1 and date2:
        return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day
    return False


def last_time_of_day(date):
    return datetime(date.year, date.month, date.day, hour=23, minute=59, second=59)


def get_days(start, end):
    '''
    获取开始和结束之间的所有日期
    '''
    if start > end:
        temp = start
        start = end
        end = temp
    ret = []
    while start.year != end.year or start.month != end.month or start.day != end.day:
        ret.append(start)
        start = start + timedelta(days=1)
    ret.append(end)
    return ret


def week_start_end(date=datetime.now()):
    '''
    返回date所在周的开始和结束时间
    '''
    week_day = date.weekday()  # week_day从0到6，0为周一
    start_day = date - timedelta(days=week_day)
    end_day = date + timedelta(days=(6 - week_day))
    start_day = datetime(year=start_day.year, month=start_day.month, day=start_day.day, hour=0, minute=0, second=0)
    end_day = datetime(year=end_day.year, month=end_day.month, day=end_day.day, hour=23, minute=59, second=59)
    return start_day, end_day
