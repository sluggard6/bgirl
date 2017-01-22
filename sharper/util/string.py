# -*- coding:utf-8 -*-
"""
    util/string.py
    ~~~~~~~~~~~~~~

    string util
"""
import hashlib
import random
import re
import uuid


def md5(_str, length=32):
    """
    md5 hash并返回指定长度位数的串
    """
    if length <= 0 or length > 32:
        length = 32
    return hashlib.md5(_str).hexdigest()[:length]


def random_number(length):
    """
    获取指定长度的随机数字串 length<100
    """
    return ''.join(random.sample('0123456789' * 10, length))


def random_ennum(length):
    """
    获取指定长度的随机英文字符+数字串 length<100
    """
    if length <= 0 or length > 100:
        length = 100
    return ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz' * 4, length))


def random_en(length):
    """
    获取指定长度的随机英文字符+数字串 length<100
    """
    if length <= 0 or length > 100:
        length = 100
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz' * 4, length))


def check_special_sign(signs):
    import re

    clear = re.compile(u'[\;\:\\\'\.\/\,\!\`\?\~\^\&\*\$\|\(\)\<\>\{\}\+\%\-\[\]=@#"～！·＃￥…&＊（）—｛｝、】【：“”；‘’，。、？》《]')
    return clear.search(signs) is not None


def verify_username(name, charset='utf8'):
    """
    检查用户名是否规范 英文数字中文 禁止标点符号
    @param name: 用户名
    @return:
    """
    import re

    if not isinstance(name, unicode):
        name = name.decode(charset)
    return re.compile(ur'^[a-zA-Z0-9\u3400-\u4DB5\u4E00-\u9FFF\uF900-\uFAD9]{2,16}$').match(name) is not None


def is_camel(_str):
    """
    判断字符串是否驼峰拼写规则
    """
    return re.compile(r'^[A-Z][A-Za-z0-9]+$').match(_str) is not None


def html_filter(html):
    """过滤html标签，返回文本"""
    from BeautifulSoup import BeautifulSoup

    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        tag.hidden = True
    return soup.renderContents(prettyPrint=True)


def gen_4_4_id():
    """
    随机产生4×4 dash 分割数字英文字符串
    713d-e675-49f1-b0f2
    """
    return '-'.join([s[:4] for s in str(uuid.uuid4()).split('-')][0:4])


def to_camel_case(name):
    if name.find("_") != -1:
        names = name.split("_")
        new_name = ""
        for n in names:
            new_name += n.title()
        return new_name
    return name.title()

