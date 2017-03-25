# -*- coding:utf-8 -*-
import base64
import os


__author__ = [
    '"liubo" <liubo@51domi.com>'
]


class RSASigner():
    def __init__(self, app_id):
        from Crypto.PublicKey import RSA
        from luhu_biz.orm.coop_app import CoopApp

        if app_id == "luhu":
            public_key = open('%s/keys/luhu_rsa_public_key.pem' % os.path.split(os.path.realpath(__file__))[0],
                              'r').read()
        else:
            public_key = CoopApp.get(app_id).public_key
        self.public_key = RSA.importKey(public_key)
        self.private_key = RSA.importKey(
            open('%s/keys/luhu_rsa_private_key.pem' % os.path.split(os.path.realpath(__file__))[0],
                 'r').read())

    def sign(self, message):
        '''
        @param message: 需要签名的字符串
        '''
        from Crypto.Hash import SHA
        from Crypto.Signature import PKCS1_v1_5 as pk
        from Crypto.Random import atfork

        atfork()
        digest = SHA.new(message)
        signer = pk.new(self.private_key)
        signed_message = signer.sign(digest)
        signed_message = base64.b64encode(signed_message)
        return signed_message

    def verify(self, message, sign):
        from Crypto.Hash import SHA
        from Crypto.Signature import PKCS1_v1_5 as pk

        sign = base64.b64decode(sign)
        verifier = pk.new(self.public_key)
        if verifier.verify(SHA.new(message), sign):
            return True
        else:
            return False

