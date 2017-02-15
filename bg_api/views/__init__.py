# -*- coding:utf-8 -*-
from default import DefaultView, error_handler
from user import UserView
from pic import PicView
from group import GroupView
from views.channel import ChannelView

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
