# -*- coding:utf-8 -*-
"""
    lib/TypedMediaUploader.py
    ~~~~~~~~~~~~~~

    typed media uploader

    :author: linnchord@gmail.com
    :date:2011-10-10

"""
import os
import luhu_sharper
from luhu_sharper.util import file, imgtool
from flask import current_app
from luhu_sharper.lib.error import UploadFailedError
from luhu_sharper.lib.error import UploadTypeError
from luhu_sharper.util.file import allowed_file_ext, get_file_fix, gen_random_dir, gen_random_filename, mkdirs
from luhu_sharper.util.imgtool import zoom, square


def do(file, seed, media_type, config=None):
    if not config: config = current_app.config['UPLOAD_HANDLER']
    if not file:
        raise UploadFailedError(u'上传文件失败')

    file_name = file.filename.lower()
    if not allowed_file_ext(file_name, config[media_type]['allowed_ext']):
        raise UploadTypeError(
            u'上传文件（%s）类型错误，仅允许 %s 文件' % (file_name, ','.join(config[media_type]['allowed_ext']).strip(',')))

    uri, abs_uri = gen_random_path(media_type, file_name, seed)
    file.save(abs_uri)

    if config[media_type].get('handlers'):
        for handler in config[media_type]['handlers']:
            make_media(abs_uri, config[media_type]['handlers'][handler])

    return uri


def make_media(file_path, conf):
    """
    根据配置处理指定地址的图片

    config={'method':'zoom|square', 'long':1280, 'short':500, 'side':320, 'ext':'standard'}

    method:     zoom    缩放
                square   正方形剪切

    long|short: 允许一个参数，表示按长边或短边缩放

    side:       method为square此参数指定正方形边长

    ext:        指定处理后图片添加扩展名 xxxxxxxxxxx.ext.jpeg
    """
    new_path = get_file_fix(file_path, conf['ext']) if conf.get('ext') else file_path

    if conf['method'] == 'zoom':
        if conf.get('long'):
            zoom(file_path, new_path, long=conf['long'])
        elif conf.get('short'):
            zoom(file_path, new_path, short=conf['short'])

    elif conf['method'] == 'square':
        square(file_path, new_path, conf['side'])


def get_http_ref(media_type):
    return current_app.config['UPLOAD_REF_URI'] + '/' + media_type + '/'


def get_media_handler_ext_fix_path(file_path, media_type, handler):
    ext = current_app.config['UPLOAD_HANDLER'][media_type]['handlers'][handler].get('ext')
    return get_file_fix(file_path, ext) if ext else file_path


def load_handler_conf(media_type):
    return current_app.config['UPLOAD_HANDLER'][media_type]['handlers']


def gen_random_path(media_type, file_name, seed=None):
    """
    根据类型生成随机文件路径，自动创建目录路径
    """
    save_dir = current_app.config['UPLOAD_HANDLER'][media_type]['upload_folder']
    random_dir = gen_random_dir(seed)
    random_filename = gen_random_filename(file_name, seed)
    abs_dir = os.path.join(save_dir, random_dir)
    mkdirs(abs_dir)
    uri = os.path.join(random_dir, random_filename)
    return uri, os.path.join(save_dir, uri)
