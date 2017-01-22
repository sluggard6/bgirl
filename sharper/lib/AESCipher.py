# -*- coding:utf-8 -*-
import base64
from Crypto import Random
from Crypto.Cipher import AES

__author__ = [
    '"liubo" <liubo@51domi.com>'
]

PADDING = '\0'
# PADDING = ' '
pad_it = lambda s: s + (16 - len(s) % 16) * PADDING
unpad = lambda s: s[0:-ord(s[-1])]

class AESCipher:
    def __init__(self, key):
        Random.atfork()
        self.key = key
        self.iv = "1234567812345678"

    def encrypt(self, raw):
        generator = AES.new(self.key, AES.MODE_CBC, self.iv)
        crypt = generator.encrypt(pad_it(raw))
        return base64.b64encode(crypt)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.decrypt(enc).rstrip(PADDING)
