# -*- coding:utf-8 -*-
from flask import request, url_for, g, current_app
from sharper.util.string import random_ennum, md5

AUTO_LOGIN_PARAM = 'al'


def make_auto_login_cookie(resp, user, max_age=604800):
    """
    生成自动登录cookie 默认7天有效
    """
    nonce = random_ennum(8)
    token = md5(nonce + user.ucode + user.password)
    resp.set_cookie(AUTO_LOGIN_PARAM, value='%s;%s;%s' % (user.id, nonce, token), max_age=max_age)
    return resp


def check_auto_login_cookie():
    """
    验证自动登录cookie
    """
    al = request.cookies.get(AUTO_LOGIN_PARAM)
    if al:
        from giftpi_biz.user import User

        try:
            uid, nonce, token = al.split(';')
            user = User.get(uid)
            if user and md5(nonce + user.ucode + user.password) == token:
                return user
        except Exception:
            pass


def clear_auto_login_cookie(resp):
    """
    清除自动登录cookie
    """
    resp.set_cookie(AUTO_LOGIN_PARAM, expires=0)
    return resp


def full_url(endpoint, **values):
    return "%s%s" % (current_app.config.get('API_HOST'), url_for(endpoint, **values))

