# -*- coding:utf-8 -*-
from datetime import datetime
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP, Text
from luhu_sharper.flaskapp.orm.base import BaseModel


__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class Notify(BaseModel):
    __tablename__ = 'notify'
    __table_args__ = {}

    class Category(DisplayEnum):
        CONSUME = 1

        __display_cn__ = {
            CONSUME: u"支付"
        }

    class Status(DisplayEnum):
        NEW = 0
        FINISHED = 2
        PROCESSING = 1
        ERROR = -1
        __display_cn__ = {
            NEW: u"新建",
            FINISHED: u"已完成",
            ERROR: u"出错",
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    category = Column(u'category', INTEGER(), nullable=False, default=0)
    obj_id = Column(u'obj_id', INTEGER(), nullable=True, default=0)
    url = Column(u'url', VARCHAR(length=256), nullable=False)
    error_count = Column(u'error_count', INTEGER(), nullable=True, default=0)
    status = Column(u'status', INTEGER(), nullable=True, default=1)
    memo = Column(u'memo', Text(), nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)
