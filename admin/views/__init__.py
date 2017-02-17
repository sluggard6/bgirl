# -*- coding:utf-8 -*-
from flask import request

from sharper.flaskapp.helper import render_json_warn, render_json_error
from sharper.lib.error import AppError

import rq_dashboard

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
    from views.channel import ChannelView
    from views.api import ApiView
    from views.pic import PicView

    app.register_blueprint(AuthView)
    app.register_blueprint(DefaultView)
    app.register_blueprint(ManageView, url_prefix='/manage')
    app.register_blueprint(ChannelView, url_prefix='/channel')
    app.register_blueprint(ApiView, url_prefix='/api')
    app.register_blueprint(PicView, url_prefix='/pic')
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

    app.errorhandler(404)(error_handler)
    app.errorhandler(500)(error_handler)
    app.errorhandler(401)(error_handler)
    app.errorhandler(403)(error_handler)



def error_handler(e):
    """
    debug关闭后统一错误处理
    """

    if isinstance(e, AppError):
        return render_json_warn(e, request)
    else:
        return render_json_error(e, request)
