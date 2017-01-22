# -*- coding: utf-8 -*-
"""
    flaskapp/kvdb.py
    ~~~~~~~~~~~~~~
    kvdb support defined

    need config in app

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PWD = 'abc'

    REDIS_KVDB = { 'common': 0, 'session': 9 }

"""
import redis


class KVDB():
    def init_app(self, app):
        kc = app.config.get('REDIS_KVDB')
        if not kc:
            raise RuntimeError('Config "REDIS_KVDB" not found!')

        self.host = app.config.get('REDIS_HOST', '127.0.0.1')
        self.port = app.config.get('REDIS_PORT', 6379)
        self.password = app.config.get('REDIS_PASSWORD', '')

        for k in kc:

            pool = redis.ConnectionPool(host=self.host,db=kc[k],port=self.port,password=self.password,max_connections=500)

            rds = redis.Redis(connection_pool=pool)

            # rds = redis.Redis(host=self.host,
            #                   db=kc[k],
            #                   port=self.port,
            #                   password=self.password)
            setattr(self, k, rds)

        if not hasattr(self, 'common'):
            self.common = redis.Redis(host=self.host,
                                      db=0,
                                      port=self.port,
                                      password=self.password)
        if app.config.get('REDIS_JOB_HOST', None):
            self.job = redis.Redis(host=app.config.get('REDIS_JOB_HOST'),
                                   db=app.config.get('REDIS_JOB_DB', 0),
                                   port=app.config.get('REDIS_JOB_PORT', self.port),
                                   password=app.config.get('REDIS_JOB_PORT', self.password))
        return self


kvdb = KVDB()