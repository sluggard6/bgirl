# -*- coding:utf-8 -*-
import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Hash import SHA


__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


def _pkcs7padding(data):
    """
    对齐块
    size 16
    999999999=>9999999997777777
    """
    size = AES.block_size
    count = size - len(data) % size
    if count:
        data += (chr(count) * count)
    return data


def _depkcs7padding(data):
    """
    反对齐
    """
    newdata = ''
    for c in data:
        if ord(c) > AES.block_size:
            newdata += c
    return newdata


def aes_base64_encrypt(data, key):
    """
    @summary:
        1. pkcs7padding
        2. aes encrypt
        3. base64 encrypt
    @return:
        string
    """
    cipher = AES.new(key)
    return base64.b64encode(cipher.encrypt(_pkcs7padding(data)))


def base64_aes_decrypt(data, key):
    """
    1. base64 decode
    2. aes decode
    3. dpkcs7padding
    """
    cipher = AES.new(key)
    return _depkcs7padding(cipher.decrypt(base64.b64decode(data)))


def rsa_base64_encrypt(data, key):
    '''
    1. rsa encrypt
    2. base64 encrypt
    '''
    cipher = PKCS1_v1_5.new(key)
    return base64.b64encode(cipher.encrypt(data))


def rsa_base64_decrypt(data, key):
    cipher = PKCS1_v1_5.new(key)
    return cipher.decrypt(base64.b64decode(data), Random.new().read(15 + SHA.digest_size))
