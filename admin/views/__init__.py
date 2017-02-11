# -*- coding:utf-8 -*-
from flask import request
from rq_dashboard import RQDashboard

from sharper.flaskapp.helper import render_json_warn, render_json_error
from sharper.lib.error import AppError

__author__ = [
    '"liubo" <liubo@51domi.com>'
]


def register_views(app):
    """
    view注册
    """
    from views.auth import AuthView
    from views.manage import ManageView
    from views.default import DefaultView
    app.register_blueprint(AuthView)
    app.register_blueprint(DefaultView)
    app.register_blueprint(ManageView, url_prefix='/manage')
    RQDashboard(app, url_prefix='/rq')

    app.error_handler_spec[None][500] = error_handler
    app.error_handler_spec[None][404] = error_handler
    app.error_handler_spec[None][401] = error_handler
    app.error_handler_spec[None][403] = error_handler


def error_handler(e):
    """
    debug关闭后统一错误处理
    """

    if isinstance(e, AppError):
        return render_json_warn(e, request)
    else:
        return render_json_error(e, request)
