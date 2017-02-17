# -*- coding:utf-8 -*-
import sys;

reload(sys);
sys.setdefaultencoding('utf-8')
import logging
import os
from datetime import datetime
from flask import g, Flask, request, abort, session, flash, redirect, current_app

app = Flask(__name__)


def load_config(app):
    """
    加载配置
    """
    ver_map = dict(dev='Development', beta='Beta', release='Release')
    dir_ver = os.path.abspath('.').split('_')[-1]

    if dir_ver in ver_map:
        app.config.from_object('config.config.' + ver_map[dir_ver])
    else:
        try:
            app.config.from_object('config.local.Local')
        except ImportError:
            app.config.from_object('config.config.Production')

    luhu_lib_dir = app.config.get('LUHU_LIB_DIR', '/usr/bgirl/lib')
    # if dir_ver in ver_map:
    # luhu_lib_dir += '/' + dir_ver

    if luhu_lib_dir not in sys.path:
        sys.path.insert(1, luhu_lib_dir)

    from sharper.flaskapp.logger import logger, init_logger

    init_logger(app.config.get('APP_LOG_FILE'))
    if app.config.get('LOG_DEBUG'):
        logger.setLevel(logging.DEBUG)

    if app.config.get('ENABLE_HTTPS'):
        app.current_http = 'https://'
    else:
        app.current_http = 'http://'
    app.current_http_domain = app.current_http + app.config.get('DOMAIN')


def init_app(app):
    """
    app初始化
    """
    load_config(app)

    from lib.extensions import assets
    from sharper.flaskapp.mail import mail
    from sharper.flaskapp.orm.base import db
    from sharper.flaskapp.kvdb import kvdb
    from sharper.flaskapp.redis_session import RedisSessionJsonInterface

    kvdb.init_app(app)
    db.init_app(app)
    db.app = app
    assets.init_app(app)
    mail.init_app(app)
    
    
    
    app.session_interface = RedisSessionJsonInterface(kvdb.session)

    from lib.template import init_template

    init_template(app)

    from views import register_views

    register_views(app)

    from sharper.flaskapp.recaptcha import init_recaptcha

    init_recaptcha(app)


init_app(app)


@app.before_request
def init_request():
    # 构建c变量 用于作为json写入客户端app变量
    from sharper.lib.dict_proxy import DictProxyObject

    g.c = DictProxyObject()
    g.now = datetime.now()

    g.is_login = False
    g.download_host = current_app.config['DOWNLOAD_HOST']
    if request.path not in ("/login", "/logout", "/", "/recaptcha") and not request.path.startswith(
            "/project-manager") and not request.path.startswith("/static") and not request.path.startswith(
            "/api/upload"):
        from views.auth import get_auto_login_token, login_session
        from bg_biz.orm.admin import AdminUser

        user_id = session.get('user_id') or 0
        if user_id:
            g.me = AdminUser.get(user_id)
            if not g.me or not g.me.status:
                flash(u'用户已经被禁用！', 'warn')
                return redirect('/logout')
            else:
                g.is_login = True
        else:
            from views.auth import AUTO_LOGIN_COOKIE_NAME

            token = request.cookies.get(AUTO_LOGIN_COOKIE_NAME)
            if token:
                user_id, hs = token.split('_')
                g.me = AdminUser.get(int(user_id))

                if g.me and g.me.status and token == get_auto_login_token(g.me):
                    login_session(g.me)
                else:
                    session['return_url'] = request.url
                    return redirect('/logout')
            else:
                session['return_url'] = request.url
                return redirect('/')

        from lib.decorator import init_guide

        init_guide(g.me)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8270)
