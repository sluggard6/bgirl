# -*- coding:utf-8 -*-
from bg_biz.orm.pic import Group, Channel
from flask import Blueprint, g, request
from bg_biz.service.pic_service import pic_build
from sharper.util.transfer import orm_obj2dict

__author__ = [
    'wufang'
]

ChannelView = Blueprint('channel', __name__)

@ChannelView.route('/list', methods=['POST', 'GET'])
def channel_list():
    channels = Channel.query.all()
    return g.ret_success_func(channels=[orm_obj2dict(channel) for channel in channels])
