# -*- coding:utf-8 -*-
from sharper.flaskapp.kvdb import kvdb
from sharper.flaskapp.orm.base import BaseModel, db
from sharper.flaskapp.orm.display_enum import DisplayEnum
from sharper.flaskapp.orm.kvdb_mixin import KvdbMixin
from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, Table, ForeignKey

from sqlalchemy.orm import relation
from bg_biz.utils import get_download_url
from datetime import datetime

__author__ = [
    'sluggard'
]

metadata = BaseModel.metadata

_kvdb = kvdb.common

group_channel_mapping = Table(u'group_channel_mapping', metadata,
                              Column(u'group_id', INTEGER(), ForeignKey('group.id'), primary_key=True, nullable=False),
                              Column(u'channel_id', INTEGER(), ForeignKey('channel.id'), primary_key=True,
                                     nullable=False),
                              )

group_pic_mapping = Table(u'group_pic_mapping', metadata,
                          Column(u'group_id', INTEGER(), ForeignKey('group.id'), primary_key=True, nullable=False),
                          Column(u'pic_id', INTEGER(), ForeignKey('pic.id'), primary_key=True,
                                 nullable=False),
                          )


class Channel(BaseModel):
    __tablename__ = 'channel'

    __table_args__ = {}

    class Status(DisplayEnum):
        AVAILABLE = 1
        DISABLE = 0

        __display_cn__ = {
            AVAILABLE: u'有效',
            DISABLE: u'无效'
        }

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(u'name', VARCHAR(length=50), nullable=False)
    description = Column(u'description', VARCHAR(length=200))
    pid = Column(u'pid', INTEGER(), default=0)
    thumb = Column(u'thumb', VARCHAR(length=200))
    status = Column(u'status', INTEGER(), nullable=False, default=1)

    group = relation('Group',
                     primaryjoin='Channel.id==group_channel_mapping.c.channel_id',
                     secondary=group_channel_mapping,
                     secondaryjoin='group_channel_mapping.c.group_id==Group.id')

    def _clear_all_groups(self):
        db.engine.execute('DELETE FROM group_channel_mapping WHERE channel_id=%s', self.id)

    def update_groups(self, group_id_list):
        self._clear_all_groups()
        if group_id_list:
            db.engine.execute(group_channel_mapping.insert(), [
                dict(channel_id=self.id, group_id=rid) for rid in group_id_list
                ])
    @property
    def pics(self):
        pics =[]
        for g in self.group:
            print g
            for pic in g.pics:
                print pic
                pics.append(pic)
        print pics
        return pics


class Group(BaseModel, KvdbMixin):
    __tablename__ = 'group'

    __table_args__ = {}

    class Status(DisplayEnum):
        AVAILABLE = 1
        DISABLE = 0

        __display_cn__ = {
            AVAILABLE: u'有效',
            DISABLE: u'无效'
        }

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(u'name', VARCHAR(length=25), nullable=False)
    description = Column(u'description', VARCHAR(length=200))
    thumb = Column(u'thumb', VARCHAR(length=200))
    thumb2 = Column(u'thumb2', VARCHAR(length=200))
    thumb3 = Column(u'thumb3', VARCHAR(length=200))
    supplier_id =Column(u'supplier_id',VARCHAR(length=45))
    shoot_time = Column(u'shoot_time',DATETIME(),default=datetime.today())
    group_no = Column(u'group_no',VARCHAR(length=45))
    status = Column(u'status', INTEGER(), nullable=False, default=Status.AVAILABLE)

    channels = relation('Channel',
                        primaryjoin='Group.id==group_channel_mapping.c.group_id',
                        secondary=group_channel_mapping,
                        secondaryjoin='group_channel_mapping.c.channel_id==Channel.id')

    pics = relation('Pic',
                        primaryjoin='Group.id==group_pic_mapping.c.group_id',
                        secondary=group_pic_mapping,
                        secondaryjoin='group_pic_mapping.c.pic_id==Pic.id')


    def _clear_all_pics(self):
        db.engine.execute('DELETE FROM group_pic_mapping WHERE group_id=%s', self.id)

    def _clear_all_channels(self):
        db.engine.execute('DELETE FROM group_channel_mapping WHERE group_id=%s', self.id)

    def update_pics(self, pic_id_list):
        self._clear_all_pics()
        if pic_id_list:
            db.engine.execute(group_pic_mapping.insert(), [
                dict(group_id=self.id, pic_id=rid) for rid in pic_id_list
                ])

    def update_channels(self, channel_id_list):
        self._clear_all_channels()
        if channel_id_list:
            db.engine.execute(group_channel_mapping.insert(), [
                dict(group_id=self.id, channel_id=rid) for rid in channel_id_list
                ])

    @property
    def thumb_http(self):
        return get_download_url('image',self.thumb)

    @property
    def thumb2_http(self):
        return get_download_url('image',self.thumb2)
    @property
    def thumb3_http(self):
        return get_download_url('image',self.thumb3)



class Pic(BaseModel, KvdbMixin):
    __tablename__ = 'pic'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    title = Column(u'title', VARCHAR(length=45), nullable=True)
    min = Column(u'min', VARCHAR(length=200), nullable=False)
    normal = Column(u'normal', VARCHAR(length=200), nullable=False)
    max = Column(u'max', VARCHAR(length=200), nullable=False)
    create_time = Column(u'create_time', DATETIME(), nullable=False, default=datetime.now())
    modify_time = Column(u'modify_time', DATETIME(), nullable=False, default=datetime.now())

    @property
    def d_normal(self):
        return get_download_url('image',self.normal)

    @property
    def d_min(self):
        return get_download_url('image',self.min)

    @property
    def d_max(self):
        return get_download_url('image',self.max)


class Supplier(BaseModel):
    __tablename__ ='supplier'

    __table_args__={}

    class Status(DisplayEnum):
        AVAILABLE = 1
        DISABLE = 0

        __display_cn__ = {
            AVAILABLE: u'有效',
            DISABLE: u'无效'
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    name = Column(u'name', VARCHAR(length=100), nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=False, default=datetime.now())
    update_time = Column(u'update_time', DATETIME(), nullable=False, default=datetime.now())
    description = Column(u'description', VARCHAR(length=200))
    status = Column(u'status', INTEGER(), nullable=False, default=Status.AVAILABLE)

    @classmethod
    def suppliers(cls):
        list = Supplier.query.filter_by(status=1).all()
        return list
