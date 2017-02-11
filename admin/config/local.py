# -*- coding:utf-8 -*-
"""

    config/config.py
    ~~~~~~~~~~~~~~

    系统配置

    定义开发机本地配置

    * 同目录下创建local.py
    * local.py中

        from config import Development
        class Local(Development):
            DEBUG=True
            ...

"""

from config import Development


class Local(Development):
    DEBUG = True
    LUHU_LIB_DIR = '/home/cyh/work/pyweb/'
    APP_LOG_FILE = '/Users/john/git/bgirl/admin/bg_admin.log'
    WORKER_LOG_FILE = '/home/cyh/work/pyweb/log/hiwifi/rq_worker.log'
    REDIS_HOST = '123.206.15.218'
    REDIS_JOB_HOST = '123.206.15.218'
    REDIS_URL = 'redis://123.206.15.218:6379/0'
    REDIS_PASSWORD = 'crs-oj7t4z7i:hiwifi@2016'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin1234@127.0.0.1:3306/bgirl'
    SQLALCHEMY_BINDS = {
        'data': 'mysql://root:admin1234@127.0.0.1:3306/bgirl'
    }
