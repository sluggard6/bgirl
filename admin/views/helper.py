# -*- coding:utf-8 -*-
from sharper.flaskapp.helper import get_flash_msg
from bg_biz.orm.admin import AdminUser


def get_admin(admin_id):
    return AdminUser.get(admin_id)


def get_phones(phone_str):
    return phone_str.replace(u"，", ",") \
        .replace(u";", ",").replace("，", ",").replace(" ", ",") \
        .replace("\r\n", ",").replace("\n", ",").split(",")