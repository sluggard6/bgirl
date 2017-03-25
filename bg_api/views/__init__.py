# -*- coding:utf-8 -*-
from default import DefaultView, error_handler
from user import UserView
from pic import PicView
from group import GroupView
from channel import ChannelView
from page import PageView
from pay import PayView
from charge import ChargeView

__author__ = [
    "sluggrd"
]


def register_views(app):
    from default import DefaultView, error_handler

    app.errorhandler(404)(error_handler)
    app.errorhandler(500)(error_handler)
    app.errorhandler(401)(error_handler)
    app.errorhandler(403)(error_handler)

    app.register_blueprint(DefaultView)
    app.register_blueprint(UserView, url_prefix='/user')
    app.register_blueprint(PicView, url_prefix='/pic')
    app.register_blueprint(GroupView, url_prefix='/group')
    app.register_blueprint(ChannelView, url_prefix='/channel')
    app.register_blueprint(PageView, url_prefix='/page')
    app.register_blueprint(PayView,url_prefix='/pay')
    app.register_blueprint(ChargeView,url_prefix='/charge')
