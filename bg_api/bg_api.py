# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import os
from flask import Flask, g


app = Flask(__name__)


def load_config(app):
    """
    加载配置
    """
    ver_map = dict(dev='Development', beta='Beta', release='Release')
    dir_ver = os.path.abspath('.').split('_')[-1]

    if dir_ver in ver_map:
        app.config.from_object('config.config.' + ver_map[dir_ver])
        app.config['deploy_version'] = dir_ver
    else:
        try:
            app.config.from_object('config.local.Local')
        except ImportError:
            app.config.from_object('config.config.Production')

    lib_dir = app.config.get('LIB_DIR', '/usr/bgirl/lib')
    if lib_dir not in sys.path:
        sys.path.append(lib_dir)

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

    from sharper.flaskapp.orm.base import db
    from sharper.flaskapp.kvdb import kvdb
    from sharper.flaskapp.redis_session import RedisSessionInterface
    from sharper.flaskapp.login import init_login
    from lib.logger_client import init_logger_client, init_pay_logger_client

    kvdb.init_app(app)
    # producer.init_app(app)
    db.init_app(app)
    db.app = app
    init_logger_client(app)
    init_pay_logger_client(app)
    app.session_interface = RedisSessionInterface(kvdb.session)
    init_login(app)

    from lib.template import init_template

    init_template(app)
    from lib.extensions import assets

    assets.init_app(app)
    from views import register_views

    register_views(app)


init_app(app)


@app.before_request
def init_request():
    from lib.decorator import do_switch_ret
    do_switch_ret()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8290, use_reloader=True)

