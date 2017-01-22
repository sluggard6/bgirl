# -*- coding:utf-8 -*-
import simplejson as json
import time

__author__ = [
    '"liubo" <liubo@51domi.com>'
]
__date__ = '12-6-26'

ACCESS_KEY = "byHmrKJvxM9q8OSFXkTv69kRcDHAuRMcPbq2N5sO"
SECRET_KEY = "m0IFnfXICSRQxMGnMqRn_9lMIglRAknWKCiSZVM8"


class AuthPolicy(object):
    def __init__(self, scope='', callback_url='', return_url='', expires_in=30 * 24 * 3600):
        self.scope = scope
        self.callback_url = callback_url
        self.return_url = return_url
        self.deadline = expires_in + int(time.time())

    def marshal(self):
        obj={}
        obj['scope']=self.scope
        if self.callback_url:
            obj['callbackUrl']=self.callback_url
        if self.return_url:
            obj['returnUrl']=self.return_url
        obj['deadline']=self.deadline
        return json.dumps(obj,separators=(',',':'))

    def make_token(self):
        from hashlib import sha1
        from hmac import new
        import base64
        policy_json=self.marshal()
        policyBase64 = base64.urlsafe_b64encode(policy_json)
        mac = new(SECRET_KEY, policyBase64, sha1)
        digest = base64.urlsafe_b64encode(mac.digest())
        return "%s:%s:%s"%(ACCESS_KEY,digest,policyBase64)

