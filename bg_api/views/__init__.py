# -*- coding:utf-8 -*-
from default import DefaultView, error_handler


__author__ = [
    '"liubo" <liubo@51domi.com>'
]


def register_views(app):
    from default import DefaultView, error_handler

    app.error_handler_spec[None][500] = error_handler
    app.error_handler_spec[None][404] = error_handler
    app.error_handler_spec[None][401] = error_handler
    app.error_handler_spec[None][403] = error_handler

    app.register_blueprint(DefaultView)
