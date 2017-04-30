# -*- coding:utf-8 -*-


import os
from PIL import Image



__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


if __name__ == '__main__':
    from bg_admin import app

    ctx = app.test_request_context()
    ctx.push()

    from sharper.util.imgtool import square, zoom

    from bg_biz.orm.pic import Pic

    #prefix = "/var/www/upload/image/"
    prefix = "/Users/john/git/upload/image/"
    for pic in Pic.query.all():
        path = "%s%s" % (prefix, pic.normal)
        new_path = "%smin/%s" % (prefix, pic.normal)

        if os.path.exists(path):
            try:
                w, h = Image.open(path).size
                if w > 800:
                    zoom(path, new_path, long=800)
                    print path
            except Exception as e:
                print e
                print "error", path
                continue
