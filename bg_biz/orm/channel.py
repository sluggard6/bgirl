# -*- coding:utf-8 -*-
"""大本营基础系统"""
import cPickle as pickle
from datetime import datetime

from flask import current_app
from sqlalchemy import *
from sqlalchemy.orm import relation
from werkzeug.utils import cached_property

from bg_biz.signals import admin_rup_changed
from sharper.flaskapp.kvdb import kvdb
from sharper.flaskapp.orm.base import BaseModel, db
from sharper.lib.error import AppError
from sharper.util import helper, string

__authors__ = ['John Chan']

metadata = BaseModel.metadata

_kvdb = kvdb.common

group_channel_mapping = Table(u'group_channel_mapping', metadata,
                              Column(u'group_id', INTEGER(), ForeignKey('group.id'), primary_key=True, nullable=False),
                              Column(u'channel_id', INTEGER(), ForeignKey('channel.id'), primary_key=True,
                                     nullable=False),
                              )


class Channel(BaseModel):
    __tablename__ = 'channel'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(u'name', VARCHAR(length=50), nullable=False)
    description = Column(u'description', VARCHAR(length=200))
    pid = Column(u'pid', INTEGER(), default=0)
    thumb = Column(u'thumb', VARCHAR(length=200))
    status = Column(u'status', Integer(), nullable=False, default=1)

    group = relation('Group',
                     primaryjoin='Channel.id==group_channel_mapping.c.channel_id',
                     secondary=group_channel_mapping,
                     secondaryjoin='group_channel_mapping.c.group_id==Group.id')

    def _clear_all_groups(self):
        db.engine.execute('DELETE FROM group_channel_mapping WHERE channel_id=%s', self.id)

    def update_groups(self, group_id_list):
        """
        批量更新角色到用户
        @param role_id_list: 角色id列表
        @return:
        """
        self._clear_all_groups()
        if group_id_list:
            db.engine.execute(group_channel_mapping.insert(), [
                dict(channel_id=self.id, group_id=rid) for rid in group_id_list
                ])


class Group(BaseModel):
    __tablename__ = 'group'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(u'name', VARCHAR(length=25), nullable=False)
    description = Column(u'description', VARCHAR(length=200))
    status = Column(u'status', Integer(), nullable=False, default=1)

    admin_users = relation('Channel',
                           primaryjoin='Group.id==group_channel_mapping.c.group_id',
                           secondary=group_channel_mapping,
                           secondaryjoin='group_channel_mapping.c.channel_id==Channel.id')
