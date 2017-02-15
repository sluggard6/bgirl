# -*- coding:utf-8 -*-
import os
from flask import current_app

__author__ = [
    'sluggard'
]


def get_download_url(type, path):
    if path:
        return current_app.config.get("DOWNLOAD_HOST") + type + os.sep + path
    return None
