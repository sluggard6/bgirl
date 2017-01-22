# -*- coding:utf-8 -*-
"""
模版自定义过滤器
"""
import cgi
import os
from datetime import datetime, date
from flask import current_app
from urllib import quote, quote_plus
import re
from sharper.flaskapp.kvdb import kvdb
from sharper.util import string
from ..util.string import html_filter
from .logger import logger
from ..util.transfer import strftime


_CACHE = {}


def safe_enter2br(s):
    """预览文本 换行替换"""
    return cgi.escape(s).replace("\n", "<br/>") if s else ''


def safe_enter2p(s):
    """正文 换行替换"""
    return '<p>' + cgi.escape(s).replace("\n", "</p><p>") + '</p>' if s else ''


def safe_enter2li(s):
    """正文 换行替换"""
    return '<li>' + cgi.escape(s).replace("\n", "</li><li>") + '</li>' if s else ''


def filter_safe_enter_preview(s):
    """预览文本 换行替换"""
    return cgi.escape(s).replace("\n", "<br/>")


def filter_safe_enter(s):
    """正文 换行替换"""
    return '<p>' + cgi.escape(s).replace("\n", "</p><p>") + '</p>'


def filter_enter(s):
    """正文 换行替换"""
    s = s.replace("\n", "<br/>")
    return s.replace(" ", "&nbsp")


def static(filepath, add_timer=True):
    """
    自动为静态path路径添加时间戳 - 进程内缓存
    """
    from flask import request

    STATIC_HTTP_REF = current_app.config.get('STATIC_HTTP_REF', '')

    if STATIC_HTTP_REF:
        from sharper.flaskapp.helper import get_https_url

        if request.scheme == 'https':
            STATIC_HTTP_REF = get_https_url(STATIC_HTTP_REF)

    return _CACHE.setdefault(
        (request.scheme + filepath),
        STATIC_HTTP_REF + filepath + (
            '?' + datetime.fromtimestamp(
                os.path.getmtime(current_app.root_path + filepath)
            ).strftime('%Y%m%d%H%M%S') if add_timer else ''
        )
    )


def do_urlencode(value, plus=False):
    """
    url编码filter
    """
    if isinstance(value, unicode):
        value = value.encode('utf8')
    return quote_plus(value) if plus else quote(value)


def remove_html_tag(_str):
    if _str:
        return html_filter(_str)
    else:
        return None


def date2str(d, format='%Y-%m-%d'):
    """
    format the datetime to string
    """
    try:
        if isinstance(d, datetime):
            return strftime(d, fmt=format)
        elif isinstance(d, date):
            return strftime(d, fmt=format)
        elif isinstance(d, int):
            return strftime(datetime.fromtimestamp(d))
    except Exception as ex:
        logger.warn(ex)

    return str(d)


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


def max_length(str, max_len):
    if str:
        if max_len <= 3:
            return str[:max_len]
        import unicodedata

        s = 0
        count = 0
        for ch in str:
            if isinstance(ch, unicode):
                if unicodedata.east_asian_width(ch) != 'Na':
                    s += 2
                else:
                    s += 1
            else:
                s += 1
            count += 1
            if s >= max_len:
                return str[:count] + ".."
    return str


def emoji(text):
    """
    表情文本处理
    """
    pattern = re.compile('\[([^\s\+\-_\]\[]+)\]')
    emoji_list = current_app.config['EMOJI_LIST']

    def make_emoji(m):
        name = m.group(1)
        if name not in emoji_list:
            return '[%s]' % name
        tpl = """
            <img class="emoji" style="width:auto" title="%s" src="http://static.hi-wifi.cn/emoji/%s.png" align="top">"""
        return tpl % (name, emoji_list[name]['en'])

    text = pattern.sub(make_emoji, text) if text else ''
    return text


_CACHE = {}

CACHE_DEFAULT_DURATION = 2592000  #默认缓存 1个月


def content_render(s):
    """
    文本全文转换浏览 cached
    """

    def do(t):
        return emoji(filter_safe_enter(t))

    return build_text_from_cache(s, do)


def content_render_flow(s, length=100):
    """
    瀑布流中文本转换渲染 cached
    """

    def do(t):
        #删除文本末尾可能出现未能完整截取的表情字符
        p = re.compile('\[[^\s\[\]]{0,16}$')
        txt = p.sub('', t[:length])
        return emoji(filter_safe_enter_preview(txt)) + (' ...' if len(t) > length else '')

    return build_text_from_cache(s, do, length)


def do_urlencode(value, plus=False):
    """
    url编码filter
    """
    if isinstance(value, unicode): value = value.encode('utf8')
    return quote_plus(value) if plus else quote(value)


def build_text_from_cache(s, func, seed=None):
    """
    从cache获取文本处理结果, 用于模板文本渲染过滤
        s: 文本
        seed: 缓存参数
        handler: 处理函数
    """
    key = 'luhu:text_cache:' + string.md5(s) + (':' + str(seed) if seed else '')
    txt = kvdb.common.get(key)
    if not txt:
        txt = func(s)
        kvdb.common.setex(key, txt, CACHE_DEFAULT_DURATION)
    return txt


def content_render_thumb(s, length=14):
    if s:
        return cgi.escape(s)[:length] + (' ...' if len(s) > length else '')
    else:
        return s


def init_domi_template(app):
    app.jinja_env.line_statement_prefix = '~'
    app.jinja_env.filters['safe_enter2br'] = safe_enter2br
    app.jinja_env.filters['safe_enter2p'] = safe_enter2p
    app.jinja_env.filters['safe_enter2li'] = safe_enter2li
    app.jinja_env.filters['urlencode'] = do_urlencode
    app.jinja_env.filters['remove_html_tag'] = remove_html_tag
    app.jinja_env.filters['date2str'] = date2str
    app.jinja_env.filters['decimal_pretty'] = decimal_pretty
    app.jinja_env.filters['max_len'] = max_length
    app.jinja_env.filters['emoji'] = emoji
    app.jinja_env.filters['content_render_thumb'] = content_render_thumb
    app.jinja_env.filters['content_render_flow'] = content_render_flow
    app.jinja_env.filters['content_render'] = content_render
    app.jinja_env.globals.update(zip=zip)
    app.jinja_env.globals.update(static=static)