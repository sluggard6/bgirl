#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.04'
__author__ = 'Liao Xuefeng (askxuefeng@gmail.com)'

'''
Python client SDK for sina weibo API using OAuth 2.
'''

try:
    import simplejson as json
except ImportError:
    import json
import time_util
import md5
import urllib
import urllib2
import logging

def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)

class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

def _encode_params(**kw):
    '''
    Encode parameters.
    '''
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

def _encode_multipart(**kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time_util.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            ext = ''
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            if n != (-1):
                ext = filename[n:].lower()
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = { '.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg' }

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(url, authorization=None, **kw):
    logging.info('GET %s' % url)
    return _http_call(url, _HTTP_GET, authorization, **kw)

def _http_post(url, authorization=None, **kw):
    logging.info('POST %s' % url)
    return _http_call(url, _HTTP_POST, authorization, **kw)

def _http_upload(url, authorization=None, **kw):
    logging.info('MULTIPART POST %s' % url)
    return _http_call(url, _HTTP_UPLOAD, authorization, **kw)

def _http_call(uri, request_method, authorization, **kw):
    '''
    send an http request and expect to return a json object if no error.
    '''
    params = None
    boundary = None
    if request_method==_HTTP_UPLOAD:
        params, boundary = _encode_multipart(**kw)
    else:
        params = _encode_params(**kw)
    http_url = '%s?%s' % (uri, params) if request_method==_HTTP_GET else uri
    http_body = None if request_method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)

    if authorization:
        req.add_header('Authorization', 'OAuth2 %s' % authorization)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    resp = urllib2.urlopen(req)
    #print 'before', http_body
    body = resp.read()
    try:
        r = json.loads(body.decode('utf8', errors='ignore'), object_hook=_obj_hook)
    except ValueError:
        import urlparse
        body = urlparse.parse_qs(body)
        for k, v in body.iteritems():
            if v[0].isdigit():
                v[0] = int(v[0])
            body[k] = v[0]

        body = json.dumps(body, ensure_ascii=False)
        r = json.loads(body, object_hook=_obj_hook)

    if hasattr(r, 'error_code'):
        raise APIError(r.error_code, getattr(r, 'error_msg', ''), getattr(r,
            'request_args', ''))
    if hasattr(r, 'ret') and r['ret'] != 0:
        raise APIError(r['errcode'], getattr(r, 'msg', ''), getattr(r, 'ret', ''))
    return r

def calulate_sig(secret_key , **kw):
    sig = u''
    for k in sorted(kw.iterkeys()):
        sig += u'%s=%s' % (k, kw[k])

    sig += secret_key

    return md5.md5(sig).hexdigest()

class HttpObject(object):

    def __init__(self, client, request_method):
        self.client = client
        self.request_method= request_method

    def __getattr__(self, attr):
        def wrap(**kw):
            if self.client.is_expires():
                raise APIError('21327', 'expired_token', attr)
            if 'qq' in self.client.auth_url:
                kw['oauth_consumer_key'] = self.client.client_id
                kw['access_token'] =  self.client.access_token
                kw['oauth_version'] =  '2.a'
                kw['openid'] =  self.client.openid
                return _http_call('%s%s' % (self.client.api_url, attr.replace('__', '/')), self.request_method, self.client.access_token, **kw)
            elif 'kaixin' in self.client.auth_url:
                kw['access_token'] =  self.client.access_token
            elif 'renren' in self.client.auth_url:
                kw['format'] = 'json'
                kw['v'] = '1.0'
                kw['call_id'] = time_util.time()
                kw['access_token'] =  self.client.access_token
                kw['sig'] = calulate_sig(self.client.client_secret, **kw)
                return _http_call('%s' % (self.client.api_url), self.request_method, self.client.access_token, **kw)

            #print self.client.auth_url
            #print '%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.request_method, self.client.access_token, kw
            return _http_call('%s%s.json' % (self.client.api_url,
                attr.replace('__', '/')), self.request_method, self.client.access_token, **kw)
                #return _http_call('%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.method, self.client.access_token, **kw)
        return wrap

class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com', version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type

        if 'qq' in domain:
            self.auth_url = 'https://%s/cgi-bin/oauth2/' % domain
            self.api_url = 'https://%s/api/' % domain
        elif 'weibo' in domain:
            self.auth_url = 'https://%s/oauth2/' % domain
            self.api_url = 'https://%s/%s/' % (domain, version)
        elif 'kaixin' in domain:
            self.auth_url = 'https://%s/oauth2/' % domain
            self.api_url = 'https://%s/' % (domain)
        elif 'renren' in domain:
            self.auth_url = 'https://%s/oauth/' % domain
            self.api_url = 'http://api.renren.com/restserver.do'

        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def set_access_token(self, access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
        return the authroize url that should be redirect.
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        scope = ''
        if 'kaixin' in self.auth_url:
            scope = 'create_records'
        elif 'renren' in self.auth_url:
            scope = 'photo_upload publish_blog status_update publish_share'

        return '%s%s?%s' % (self.auth_url, 'authorize',\
                            _encode_params(client_id = self.client_id,\
                                response_type = 'code',\
                                display = display,\
                                redirect_uri = redirect,
                                scope=scope))

    def request_access_token(self, code, redirect_uri=None):
        '''
        return access token as object: {"access_token":"your-access-token","expires_in":12345678}, expires_in is standard unix-epoch-time
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        access_token = 'access_token' if 'renren' not in self.auth_url else 'token'
        r = _http_post('%s%s' % (self.auth_url, access_token),\
            client_id = self.client_id,\
            client_secret = self.client_secret,\
            redirect_uri = redirect,\
            code = code, grant_type = 'authorization_code')
        r.expires_in = int(r.expires_in) +  int(time_util.time())
        return r

    def is_expires(self):
        return not self.access_token or time_util.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)
