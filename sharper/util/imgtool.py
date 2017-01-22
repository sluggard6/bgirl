# -*- coding:utf-8 -*-
"""
    util/imgtool.py
    ~~~~~~~~~~~~~~

    simple image tools

    :author: linnchord@gmail.com
    :date:2011-10-10

"""
import shutil
from PIL import Image
from PIL.ExifTags import TAGS


def square(old_path, new_path, side):
    """
    剪切图片为正方形

    side: 边长
    """
    try:
        img = Image.open(old_path).convert('RGB')
    except IOError:
        raise IOError(u'图片格式异常，无法处理。')
    w, h = img.size

    if w != h or w > side:
        r = w if w < h else h
        offset = int(abs(w-h)/2)

        area = (offset, 0, offset+r, r) if w > h else (0, offset, r, offset+r)

        img = img.transform((r, r), Image.EXTENT, area)
        img.thumbnail((side, side), Image.ANTIALIAS)
        img.save(new_path, "JPEG", quality=85)

    elif old_path != new_path:
        img.save(new_path, "JPEG", quality=85)


def zoom(old_path, new_path, long=0, short=0, percent=0, size=()):
    """
    按原比例缩放图片
    指定缩放长边或短边，或通过比例缩放，或直接指定宽高
    """
    if percent:
        zoom_percent(old_path, new_path, percent)
        return

    img = Image.open(old_path)
    w, h = img.size

    if size:
        img.resize(size, Image.ANTIALIAS).save(new_path, "JPEG", quality=85)
        return

    percent = 1

    if long and not short:
        r = w if w > h else h
        percent = long/float(r)

    if short and not long:
        r = w if w < h else h
        percent = short/float(r)

    #如图片缩放和原图差距很小则不处理
    if 1 > (1-percent) > 0.1:
        zoom_percent(old_path, new_path, percent)
    elif new_path != old_path:
        shutil.copy2(old_path, new_path)


def zoom_percent(old_path, new_path, percent):
    """
    按比例缩放图片 - 指定百分比
    """
    img = Image.open(old_path)
    w, h = img.size
    img.resize(
        (int(w*percent), int(h*percent)),
        Image.ANTIALIAS
    ).save(new_path, "JPEG", quality=85)


def get_exif(img_path):
    ret = {}
    i = Image.open(img_path)
    info = i._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return ret


def get_genTime(img_path):
    info = get_exif(img_path)
    if info:
        return info.get('DateTimeOriginal') or info.get('DateTime')
    else:
        return None


def img_area_select(path, box, percent=1, to_path=None):
    img = Image.open(path)
    if percent != 1:
        w, h = img.size
        img = img.resize(
            (int(w*percent), int(h*percent)),
            Image.ANTIALIAS
        )
    img.crop(box).save(to_path or path)


def img_check_origin_size(img_path, size):
    img = Image.open(img_path)
    w, h = img.size
    r = w if w > h else h
    if r > size*1.2:
        percent = size/float(r)
        img.resize((int(w*percent), int(h*percent)), Image.ANTIALIAS).save(img_path, "JPEG", quality=80)


def img_resize(img_path, size, to_path):
    img = Image.open(img_path)
    w, h = img.size
    r = w if w > h else h
    if r < size:
        img.save(to_path, "JPEG", quality=80)
    else:
        percent = size/float(r)
        img.resize(
            (int(w*percent), int(h*percent)),
            Image.ANTIALIAS
        ).save(
            to_path, "JPEG", quality=80
        )
