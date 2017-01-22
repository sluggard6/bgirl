# -*- coding: utf-8 -*-
"""
    lib/web_store.py
    ~~~~~~~~~~~~~~
    网络资源存储引用
"""
import re

all_type = ('photo')
DEFAULT_CLOUD_RULE = 'qbox'

HTTP_RULE_REF = {
    'qbox': {
        'photo': "http://imghiwifi.qiniudn.com/"
    }
}


def get_uri_ref(_type, uri):
    """
    获取指定类型uri的协议、http引用、uri_key
    """
    rule, uri = get_rule(uri)
    return rule, ('http://' if rule == 'http' else HTTP_RULE_REF[rule][_type]), uri


def get_rule(uri):
    """获取uri的协议和key"""
    rx = re.compile(r'^[a-z0-9]{2,8}:\/\/').match(uri)
    return (rx.group()[:-3], uri[rx.end():]) if rx else ('local', uri)


def load_photo_http_all(url, fix=None, with_http=True, with_rule=False):
    """
    获取所有有效图片格式资源
    """
    if not url: return (None, None, None, None, None)
    rule, uri = get_rule(url)
    if rule == 'http': return (url, url, url, url, url)
    http_ref = HTTP_RULE_REF[rule]['photo'] if with_http else ''
    rule_ref = rule + '://' if with_rule else ''
    dic = dict(
        big=http_ref + rule_ref + uri,
        standard=http_ref + rule_ref + uri,
        small=http_ref + rule_ref + uri + '_s200',
        thumb=http_ref + rule_ref + uri + '_s200',
        thumb_small=http_ref + rule_ref + uri + '_s200'
    )
    if fix:
        return http_ref + rule_ref + uri + '_' + fix
    else:
        return dic['big'], dic['standard'], dic['small'], dic['thumb'], dic['thumb_small']


class QBoxImageRef(object):
    """
    qbox图片资源引用对象
    """
    def __init__(self, qbox_uri='', uri='', http_ref=''):
        if qbox_uri:
            rule, uri = get_rule(qbox_uri)
            if rule.lower() == 'qbox':
                self.http_ref = HTTP_RULE_REF[rule]['photo']
                self.uri = uri
            else:
                self.http_ref = self.uri = ''
        else:
            self.http_ref = http_ref
            self.uri = uri

        self.url = self.http_ref + self.uri

    @property
    def origin(self):
        return self.url

    @property
    def standard(self):
        return self.s350

    @property
    def small(self):
        return self.s200

    @property
    def thumb(self):
        return self.s128

    @property
    def thumb_small(self):
        return self.s64

    def __getattr__(self, name):
        """
        可自由应用图片扩展属性
        """
        return self.url + '_' + name if self.url else None
