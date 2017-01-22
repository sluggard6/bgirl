# -*- coding:utf-8 -*-
"""

    flaskapp/redis_session.py
    ~~~~~~~~~~~~~~

    Flask, session store in redis

    http://flask.pocoo.org/snippets/75/

"""
import cPickle as pickle
from datetime import timedelta, datetime
import json
from uuid import uuid4
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from .helper import get_agent


class RedisSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)

        self.sid = sid
        self.new = new
        self.modified = False
        self.permanent = True

    @classmethod
    def get_by_sid(cls, sid):
        return cls(sid=sid, new=True)


class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession
    is_client = False

    def __init__(self, redis=None, prefix='session:'):
        if redis is None: redis = Redis()
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        val = app.config.get('PERMANENT_SESSION_LIFETIME') or 1800
        return timedelta(seconds=val)

    def open_session(self, app, request):
        # agent = get_agent(request).lower()
        sid = request.args.get(app.session_cookie_name) or request.cookies.get(app.session_cookie_name)
        if not sid or sid == "null" or sid == "None":
            sid = self.generate_sid()
            return self.session_class(sid=sid)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)

        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)

        cookie_exp = self.get_expiration_time(app, session)

        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        if self.is_client:
            response.headers.add('Authorization', 'Bearer ' + session.sid)

        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)

    def _get_basic_auth_token(self, request):
        auth_str = request.headers.get('Authorization')
        if auth_str:
            lst = auth_str.split()
            if len(lst) == 2:
                title, token = lst
                if title == 'Bearer':
                    return token


class RedisSessionJsonInterface(RedisSessionInterface):
    serializer = json
    session_class = RedisSession
    is_client = False

    def __init__(self, redis=None, prefix='jsession:'):
        if redis is None: redis = Redis()
        self.redis = redis
        self.prefix = prefix
