# -*- coding:utf-8 -*-
from sharper.flaskapp.orm.base import BaseModel
from sharper.flaskapp.orm.kvdb_mixin import KvdbMixin
from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME
from bg_biz.utils import get_download_url

__author__ = [
    'sluggard'
]

class Pic(BaseModel, KvdbMixin):
    __tablename__ = 'pic'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), nullable=False,primary_key=True,autoincrement=True)
    title = Column(u'title', VARCHAR(length=45), nullable=True)
    min = Column(u'min', VARCHAR(length=200), nullable=False)
    normal = Column(u'normal', VARCHAR(length=200), nullable=False)
    max = Column(u'max', VARCHAR(length=200), nullable=False)
    create_time = Column(u'create_time', DATETIME(), nullable=False,default=None)
    modify_time = Column(u'modify_time', DATETIME(), nullable=False,default=None)


    @property
    def d_normal(self):
        return get_download_url(self.normal)

    @property
    def d_min(self):
        return get_download_url(self.min)

    @property
    def d_max(self):
        return get_download_url(self.max)

