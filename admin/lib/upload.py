# -*- coding:utf-8 -*-
import os
from random import randint
from time import time
from flask import current_app
from sharper.flaskapp import logger
from sharper.lib.error import AppError
from sharper.util.string import md5

__author__ = [
    '"liubo" <liubo@51domi.com>'
]


def upload_local(file, media_type):
    config = current_app.config['UPLOAD_HANDLER']
    if not file:
        raise AppError(u'上传文件失败')

    file_name = file.filename.lower()
    if not allowed_file_ext(file_name, config[media_type]['allowed_ext']):
         raise AppError(u'上传文件（%s）类型错误，仅允许 %s 文件' % (file_name, ','.join(config[media_type]['allowed_ext']).strip(',')))

    uri, abs_uri = gen_random_path(media_type, file_name)
    file.save(abs_uri)

    return uri


def gen_random_path(media_type, file_name, seed=None):
    """
    根据类型生成随机文件路径，自动创建目录路径
    """
    save_dir = current_app.config['UPLOAD_HANDLER'][media_type]['upload_folder']
    random_dir = gen_random_dir(seed)
    random_filename = gen_random_filename(file_name, seed)
    abs_dir = os.path.join(save_dir, random_dir)
    print 'gen_random_path------------',abs_dir
    make_dirs(abs_dir)
    uri = os.path.join(random_dir, random_filename)
    return uri, os.path.join(save_dir, uri)


def gen_random_dir(seed=None):
    seed = str(seed) if seed else str(time()) + str(randint(10000000, 99999999))
    tmp = md5(seed, 8)
    return tmp[0:2] + '/' + tmp[2:5] + '/' + tmp[5:8] + '/'


def gen_random_filename(filename, seed=None):
    seed = str(seed) if seed else str(time()) + str(randint(10000000, 99999999)) + filename
    return md5(seed, 16) + get_file_ext(filename)


def make_dirs(abs_dirs):
    if not os.path.isdir(abs_dirs):
        try:
            os.makedirs(abs_dirs)
        except OSError as e:
            print e
            logger.warn(str(e))


def allowed_file_ext(filename, list):
    return get_file_ext(filename).lower() in list


def get_file_ext(filename):
    return os.path.splitext(filename)[1]