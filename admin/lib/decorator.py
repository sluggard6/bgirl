# -*- coding:utf-8 -*-
from functools import wraps
from sharper.lib.error import AppError
from flask import session, g, request, current_app
import math

__author__ = [
    '"liubo" <liubo@51domi.com>'
]


def gen_upload_url(f):
    @wraps(f)
    def do(*args, **kwargs):
        from sharper.lib.qbox import get_upload_url

        g.upload_url = get_upload_url('giftpi_photo')[0]
        return f(*args, **kwargs)

    return do


def init_guide(cuser):
    """
    初始化用户菜单导航 - 权限配置
    @param cuser:
    @return:
    """
    g.top_permissions = cuser.top_permissions
    g.sub_permissions = dict()
    for p in g.top_permissions:
        g.sub_permissions[p.id] = cuser.sub_permissions_all(p.id)


def pagination(f):
    @wraps(f)
    def do(*args, **kwargs):
        g.page_size = 30
        page = int(request.args.get('page', 1))
        g.current_page = page
        g.real_page = page - 1

        return f(*args, **kwargs)

    return do


def permission(*permission_keys):
    """
    权限判定
    @param permission_keys: 列表 'user_edit', 'shop_info', ...
    @return:
    """

    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):
            if not g.me: raise RuntimeError(u'No login!')
            if current_app.config.get('PERMISSION_LIMIT')!="no":
                pks = list(permission_keys)
                cur_permissions = g.me.has_permissions(pks)
                if cur_permissions:
                    pass
                    """if len(cur_permissions) == 1:
                        # 当权限为单点时记录当前权限路径 - 用于菜单高亮
                        g.current_permission = session['current_permission'] = cur_permissions[0]
                    else:
                        g.current_permission = session.get('current_permission')
                    g.current_sub_permissions = g.sub_permissions[cur_permissions[0].id[:3]]"""
                else:
                    raise AppError(u'无权限访问！')
            rv = f(*args, **kwargs)
            return rv

        return func

    return decorator
