# -*- coding:utf-8 -*-
"""
    util/file.py
    ~~~~~~~~~~~~~~

    文件工具类方法
"""
import errno
from random import randint
from time import time
from sharper.util import string

__authors__ = ['"linnchord gao" <linnchord@gmail.com>']

import os


def get_file_ext(filename):
    return os.path.splitext(filename)[1]


def allowed_file_ext(filename, list):
    return get_file_ext(filename).lower() in list


def gen_random_dir(seed=None):
    seed = str(seed) if seed else str(time()) + str(randint(10000000, 99999999))
    tmp = string.md5(seed, 8)
    return tmp[0:2] + '/' + tmp[2:5] + '/' + tmp[5:8] + '/'


def gen_random_filename(filename, seed=None):
    seed = str(seed) if seed else str(time()) + str(randint(10000000, 99999999)) + filename
    return string.md5(seed, 16) + get_file_ext(filename)


def mkdirs(path):
    """
    command `mkdir -p`
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
    return True


def write_file(_file, text, model='w'):
    """
    @param _file: file object or file path
    @param text:
    @param model:
    @return:
    """
    if isinstance(_file, basestring):
        with open(_file, model) as f:
            f.write(text)

    if isinstance(_file, file):
        _file.write(text)

def get_file_fix(path, fix):
    ar = os.path.splitext(path)
    return ar[0]+'.'+fix+ar[1]
