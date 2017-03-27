# -*- coding:utf-8 -*-
"""
    flskapp/helper.py
    ~~~~~~~~~~~~~~

    Flask框架帮助方法
"""
import os
from random import randint
import traceback
import urllib2
from sharper.util.string import random_number
from flask import get_flashed_messages, request, jsonify, current_app, logging, session
import sys
from ..lib.error import ErrorCode, AppError
from ..util.helper import get_utf8, get_unicode
from .logger import logger
import time

__authors__ = ['"linnchord gao" <linnchord@gmail.com>']


def get_flash_msg(_type=None, joiner=' '):
    """
    获取指定类别所有flash消息拼接文本

    @_type: ('ok', 'info', 'warn', 'alert')
    """
    if _type:
        return joiner.join(get_flashed_messages(category_filter=[_type]))
    else:
        return joiner.join(get_flashed_messages())


def need_json_response():
    """
    判断是否需要返回json
    """
    return 'application/json' in request.headers.get('Accept')


def print_redirect(url="/", text=None, duration=5, title=u'正在跳转', templ=None):
    """
    打印内容并在指定时间（秒）跳转到指定url
    @param text:
    @param url:
    @param duration:
    @return:
    """
    if not templ:
        templ = u'<html>' \
                u'<title>{title}</title>' \
                u'<meta http-equiv="refresh" content="{duration}; url={url}" />' \
                u'<body>' \
                u'<h1>{text}</h1>' \
                u'<span>{duration}秒后将跳转，请稍候</span>' \
                u'</body>' \
                u'</html>'
    return templ.format(duration=duration, url=url, text=text, title=title)


def json_error_msg(msg, code, http_status=200):
    resp = jsonify(success=False,
                   code=code,
                   error_code=code,
                   error_msg=msg,
                   message=msg,
                   serverTime=int(1000*time.time())
    )
    resp.status_code = http_status
    return resp


def err2msg_code(err):
    if isinstance(err, AppError):
        msg = get_utf8(err.msg)
        code = err.code
    else:
        code = getattr(err, 'code', 500)
        msg = str(err)
    return msg, code


def json_error(err='', http_status=200):
    msg, code = err2msg_code(err)
    return json_error_msg(msg, code, http_status)


def json_ok(**kwargs):
    return jsonify(success=True,serverTime=int(time.time()*1000), **kwargs)


def xml_ok(**kwargs):
    if 'status' in kwargs:
        return to_xml(**kwargs)
    return to_xml(status=1, **kwargs)


def xml_error_msg(err='', **kwargs):
    return to_xml(status=0, msg=err, **kwargs)


def xml_error(**kwargs):
    return to_xml(status=0, **kwargs)


def to_xml(http_status=200, **kwargs):
    from pytoxml import PyToXml

    dic = {}
    for k in kwargs:
        dic[k] = kwargs.get(k) if kwargs.get(k) != None else ""

    resp = current_app.make_response(str(PyToXml("root", dic, xml_declaration=True).encode()))
    resp.status_code = http_status
    return resp


def render_json_warn(err, req, http_status=200):
    msg, code = err2msg_code(err)
    http_log_warn(msg, req, code)
    return json_error(err, http_status)


def render_json_error(err, req, http_status=500):
    msg, code = err2msg_code(err)
    http_log_error(msg, req, code)
    return json_error(err, http_status)


def http_log_error(msg, req, code=ErrorCode.Error):
    http_log(msg, 'error', req, code)


def http_log_warn(msg, req, code=ErrorCode.Warn):
    http_log(msg, 'warn', req, code)


def http_log_info(msg, req):
    http_log(msg, 'info', req, ErrorCode.Info)


def http_log(msg, level, req, code=500):
    log_func_map = {'error': log_error, 'warn': logger.warn, 'info': logger.info}
    if level in log_func_map:
        log_func_map[level](u'%s-%s: %s %s %s --Referrer [%s] --Agent %s' % (
            req.remote_addr,
            code,
            msg,
            req.__repr__(),
            req.form.__repr__(),
            request.headers.get('Referer', ''),
            get_agent(req)
        ))
    else:
        logger.warn('Wrong logging level!')


def log_error(msg):
    logger.error(msg)
    trac = traceback.format_exc()
    if trac and trac.strip() != 'None':
        logger.error(trac)


def get_agent(request):
    agent = request.headers.get('User-Agent') or ""
    try:
        if isinstance(agent, str):
            agent = agent.decode('utf-8')
    except:
        agent = ""
    return agent


def get_client_type():
    agent = get_agent(request)
    if not agent:
        return None
    agent = agent.lower()
    if agent.find("iphone os") != -1:
        return "ios"
    if agent.find("android") != -1:
        if agent.find("android_tv") != -1:
            return "android_tv"
        return "android"
    return "web"

def get_client_version():
    ua_infos = ua_parse()
    if ua_infos.get('os') == 'Android':

        version_code = int(ua_infos.get('client_version'))
    elif ua_infos.get('os') == 'iOS':
        version_code = int(ua_infos.get('client_version'))

    else:
        version_code = 0

    return version_code


def get_client_ip():
    return request.headers.get('X-Forwarded-For', None) or request.remote_addr


def get_cookie(key, is_urlencode=True):
    if is_urlencode:
        return urllib2.unquote(request.cookies.get(key, '').encode('utf-8')).decode('utf-8')
    else:
        return get_unicode(request.cookies.get(key, ''))


def clear_cookie(resp, name_or_list):
    """
    清除指定cookie

    @resp: response
    @name_or_list: cookie name or name list
    """
    resp = current_app.make_response(resp)
    if isinstance(name_or_list, basestring):
        name_or_list = [name_or_list]
    for n in name_or_list:
        resp.set_cookie(n, '', expires=0)
    return resp


def set_cookie(resp, name, value, expires,max_age=1800):
    """
    设置cookie
    """
    resp = current_app.make_response(resp)
    resp.set_cookie(name, value,expires=expires,max_age=max_age)
    return resp


def simple_times_limit_validate(category, key, limit=5, expire=300, _kvdb=None, more_paras=None, amount=1):
    """
    针对指定类型+关键字参数+更多其他参数（dict类型拼接）在指定过期时间内仅允许n次(limit)访问

    例如：
        * 用户登录（类型）指定ip（关键字参数）在5分钟（expire）内只允许访问5次（limit）
        * 某api指定ip或客户端在1分钟内只允许访问1000次

    @category: 类型（例如 reg | login ）
    @key: 关键参数 （例如 203.12.213.30 ）
    @limit: 限制访问次数
    @expire: 过期时间 单位：秒 通过redis key过期时间控制
    @kvdb: redis库 默认kvdb.common
    @more_paras: 用于较多参数变量控制，拼接为缓存键
    """

    # redis缓存键构造
    key = 'STLV:%s:%s' % (category, key)
    if more_paras:
        for k, v in more_paras.items():
            key += ':%s:%s' % (k, v)

    if not _kvdb:
        from .kvdb import kvdb

        _kvdb = kvdb.common

    now = _kvdb.incr(key, amount=amount)
    ttl = _kvdb.ttl(key)
    if not ttl:
        _kvdb.expire(key, expire)

    return int(now) <= limit


def simple_vcode_validate(category, key, vcode=None, expire=300, _kvdb=None, more_paras=None):
    """
    针对指定类型+关键字参数+更多其他参数（dict类型拼接）在指定过期时间设置验证码验证

    例如：
        * 用户手机绑定（类型）在5分钟（expire）内验证手机验证码

    @category: 类型（例如 reg | login ）
    @key: 关键参数 （例如 手机号 18621111111 ）
    @vcode: 验证码 （若无则生成并返回验证码，若有则验证 ）
    @expire: 过期时间 单位：秒 通过redis key过期时间控制
    @kvdb: redis库 默认kvdb.common
    @more_paras: 用于较多参数变量控制，拼接为缓存键
    """

    # redis缓存键构造
    key = 'SPV:%s:%s' % (category, key)
    if more_paras:
        for k, v in more_paras.items():
            key += ':%s:%s' % (k, v)

    if not _kvdb:
        from .kvdb import kvdb

        _kvdb = kvdb.common

    if vcode:
        if vcode == _kvdb.get(key):
            _kvdb.delete(key)
            return True
        else:
            return False
    else:
        vcode = random_number(6)
        _kvdb.setex(key, vcode, expire)
        return vcode


def is_internal_ip():
    """
    check internal ip
    """
    ip = get_client_ip()
    return (ip in current_app.config.get('INTERNAL_IP_LIST', [])
            or ip in ('127.0.0.1', '0.0.0.0')
            or ip.startswith('192.168.'))


def get_https_url(url):
    if url.startswith('https://'):
        return url
    elif url.startswith('http://'):
        return 'https' + url[4:]
    else:
        return 'https://%s/%s' % (current_app.config.get('DOMAIN'), url.strip('/'))


def get_http_url(url):
    if url.startswith('http://'):
        return url
    elif url.startswith('https://'):
        return 'http' + url[5:]
    else:
        return 'http://%s/%s' % (current_app.config.get('DOMAIN'), url.strip('/'))


def set_return_url(url):
    session['return_url'] = url


def get_return_url(default=None):
    return session.pop('return_url', default)
