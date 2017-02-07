# -*- coding:utf-8 -*-
from flask import current_app

__author__ = [
    'sluggard'
]

def get_download_url(path):
    if path:
        return current_app.config.get("DOWNLOAD_HOST") + path
    return None