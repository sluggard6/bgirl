# -*- coding:utf-8 -*-
import json
import time
import urllib
import urllib2
from datetime import datetime

from flask import Blueprint, request, jsonify, g, current_app
from sqlalchemy import or_

from lib.upload import upload_local
from sharper.flaskapp.helper import json_error
from sharper.lib.qbox import upload_web
from sharper.lib.validator import is_mobile
from sharper.util import uploader

__author__ = [
    '"liubo" <liubo@51domi.com>'
]
ApiView = Blueprint('api', __name__)


@ApiView.route("/upload/<string:media_type>", methods=['POST'])
def upload(media_type="photo"):
    data = request.form
    print data
    f = request.files['Filedata']

    print data
    package = None
    if media_type == "apk":
        key = upload_local(f, media_type)
        apk_path = "%s%s" % (current_app.config['UPLOAD_HANDLER'][media_type]['Filedata'], key)
        ret = get_local_apk_info(apk_path)
        package = ret.get('package_name')
    else:
        _seed = str(time.time())
        print '---------',_seed
        key = uploader.do(
            request.files['Filedata'],
            _seed,
            media_type,
            current_app.config['UPLOAD_HANDLER']
        )

    image_url = "%s/%s/%s" % (g.download_host, media_type, key)
    return jsonify(url=image_url,
                   thumb=image_url, package=package,
                   uri=key, fileType=media_type, original=f.filename, success=True,
                   state="SUCCESS")


@ApiView.route("/upload", methods=['POST'])
def upload_qbox():
    f = request.files['file_uploader']
    key = upload_web(f, 'imghiwifi')

    return jsonify(url="http://imghiwifi.qiniudn.com/%s_w500" % key,
                   thumb="http://imghiwifi.qiniudn.com/%s_s200" % key,
                   uri="qbox://%s" % key, fileType="jpg", original=f.filename, success=True,
                   state="SUCCESS")
