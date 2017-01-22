# -*- coding:utf-8 -*-
import os
import uuid
import config
from auth_policy import AuthPolicy

__author__ = [
    '"liubo" <liubo@51domi.com>',
    '"linnchord" <linnchord@gmail.com>'
]

from sharper.flaskapp.kvdb import kvdb

URL_CACHE_TIME = 7 * 24 * 60 * 60  #上传url缓存时间
URL_CACHE_EXPIRE_PRE_TIME = 60 * 60  #上传url提前过期时间量

_kvdb = kvdb.common


def gen_upload_token(tbname, expire=URL_CACHE_TIME):
    """
    生成upload token.
    """
    url_key = get_qbox_token_kvdb_key(tbname)
    if tbname in ('video', 'audio'):
        token = AuthPolicy(scope=tbname, callback_url=config.CONVERT_CALLBACK,
                           expires_in=URL_CACHE_TIME).make_token()
    else:
        token = AuthPolicy(scope=tbname, expires_in=URL_CACHE_TIME).make_token()

    expires_in = expire - URL_CACHE_EXPIRE_PRE_TIME
    _kvdb.setex(url_key, token, expires_in)
    return token, expires_in


def get_upload_url(tbname, refresh=False):
    """
    保留,兼容老代码，新调用请使用get_upload_token
    """
    return get_upload_token(tbname, refresh=refresh)


def get_upload_token(tbname, expire=URL_CACHE_TIME, refresh=False):
    """
    获取上传token
    """
    token_key = get_qbox_token_kvdb_key(tbname)
    token = _kvdb.get(token_key)

    if token and not refresh:
        expires_in = _kvdb.ttl(token_key)
    else:
        token, expires_in = gen_upload_token(tbname, expire)
    return token, expires_in


def get_qbox_token_kvdb_key(tbname):
    return "qbox:upload_token:" + tbname


def upload_web(file, table):
    file_name = file.filename
    if file_name.find(".") >= 0:
        file_name = file_name[file_name.rfind("."):]

    key = uuid.uuid4().get_hex() + str(file_name)
    file.save(key)
    try:
        upload_file(key, key, table=table)
    except Exception as e:
        raise e
    finally:
        os.remove(key)
    return key


def upload_file(file, key, table="imghiwifi"):
    token = get_upload_token(table)[0]
    from .rscli import PutFile

    try:
        resp = PutFile(table, key, '', str(file), 'CustomData',
                       {'key': key}, auth=token)
    except Exception as e:
        raise e


