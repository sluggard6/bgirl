# -*- coding:utf-8 -*-
"""
模版自定义过滤器
"""
from sharper.flaskapp.template import init_domi_template
from flask import current_app
from datetime import datetime
import re
import os

CACHE_DEFAULT_DURATION = 2592000        # 默认缓存 1个月
_CACHE = {}

def inject_param():
    """
    inject param in template
    """
    return dict(
        domain=current_app.config.get('HTTP_DOMAIN'),
        blank_img='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==',
    )


def convert_date_to_week(date):
    num2chinese_date = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '日'}
    return '星期%s' % num2chinese_date[date.isoweekday()]


def format_weibo_datetime(date):
    return datetime.strptime(date, "%a %b %d %H:%M:%S +0800 %Y")


def remove_br(_str):
    return (_str or '').replace("<br/>", "")


def format_content(content):
    content = re.sub('&nbsp;', '', content)
    content = re.sub(u'　', '', content)
    return re.sub('<p>[\s]*', '<p>' + '&nbsp;' * 8, content)


def flash_filter(s):
    from BeautifulSoup import BeautifulSoup

    soup = BeautifulSoup(s)
    embed = soup.find("embed")
    if embed:
        embed.replaceWith("视频暂时无法在移动设备上播放。")
    else:
        return soup
    for tag in soup.findAll("embed"):
        tag.decompose()
    return soup


def decimal_pretty(num):
    if num == 0:
        return 0
    if is_number(num):
        num = float(num)
        if num.is_integer():
            return int(num)
        else:
            return "%.2f" % num
    else:
        return num


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def date_format(s):
    if isinstance(s, datetime):
        return s.strftime("%Y-%m-%d")
    return s

def show_static(file_path, context="mobile", add_timestamp=False):
    """
    自动为静态path路径添加时间戳 - 进程内缓存
    """

    from flask import request
    if not file_path:
        return ""
    if file_path[0] != "/":
        file_path = "/" + file_path
    STATIC_HTTP_REF = current_app.config.get('CDN_STATIC_HTTP_REF', '')
    if STATIC_HTTP_REF:

        render_path = STATIC_HTTP_REF + ("/%s" % context) + file_path + (
            '?' + datetime.fromtimestamp(
                os.path.getmtime(current_app.root_path + file_path)
            ).strftime('%Y%m%d%H%M%S') if add_timestamp else ''
        )
    else:
        render_path =  STATIC_HTTP_REF + "/static" + file_path + (
            '?' + datetime.fromtimestamp(
                os.path.getmtime(current_app.root_path + file_path)
            ).strftime('%Y%m%d%H%M%S') if add_timestamp else ''
        )

    return _CACHE.setdefault(file_path, render_path)


def init_template(app):
    init_domi_template(app)
    from views import helper

    app.jinja_env.globals.update(helper=helper)
    app.context_processor(inject_param)

    app.jinja_env.filters['convert_date_to_week'] = convert_date_to_week
    app.jinja_env.filters['format_weibo_datetime'] = format_weibo_datetime
    app.jinja_env.filters['remove_br'] = remove_br
    app.jinja_env.filters['format_content'] = format_content
    app.jinja_env.filters['flash_filter'] = flash_filter
    app.jinja_env.filters['decimal_pretty'] = decimal_pretty
    app.jinja_env.filters['date'] = date_format

    app.jinja_env.globals.update(show_static=show_static)
    #app.jinja_env.globals.update(URLResolver=URLResolver)