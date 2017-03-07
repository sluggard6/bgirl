# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from bg_biz.orm.user import User, UserVcode
from sharper.flaskapp.orm.base import transaction
from sharper.lib.error import AppError

__author__ = [
    "sluggrd"
]

class UserService:
    @classmethod
    @transaction
    def register(cls, phone, password):
        if User.query.filter_by(phone=phone).first():
            return AppError(msg=u'璇ユ墜鏈哄彿鐮佸凡缁忚娉ㄥ唽')
        u = User.register(phone, password)
        return u

def validate_vcode(phone, code, category):
    """
    楠岃瘉鐮侀獙璇�
    """
    record = UserVcode.query.filter_by(phone=phone).filter_by(vcode=code).filter_by(category=category).first()
    limit_time = datetime.now() - timedelta(minutes=60)
    if record and record.status == UserVcode.Status.INIT and record.create_time > limit_time:
        record.status = UserVcode.Status.VERIFIED
        record.update()
        return True
    return False