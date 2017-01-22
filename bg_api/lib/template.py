# -*- coding:utf-8 -*-
"""
模版自定义过滤器
"""
from sharper.flaskapp.template import init_domi_template
from flask import current_app

def inject_param():
    """
    inject param in template
    """
    return dict(
        domain=current_app.config.get('HTTP_DOMAIN')
    )


def init_template(app):
    init_domi_template(app)
    from views import helper
    app.jinja_env.globals.update(helper=helper)
    # app.jinja_env.globals.update(url_resolver=URLResolver)
    app.context_processor(inject_param)

