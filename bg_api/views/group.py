# -*- coding:utf-8 -*-
from bg_biz.orm.pic import Group, Channel
from flask import Blueprint, g, request
from service.pic_service import pic_build
from sharper.util.transfer import orm_obj2dict

__author__ = [
    'wufang'
]

GroupView = Blueprint('group', __name__)

@GroupView.route('/list', methods=['POST', 'GET'])
def group():
    data = request.args or request.form
    _ids = data.get('ids')
    groups = Group.query.filter(Group.id.in_(_ids.split(','))).all()
    ret = []
    for g in groups:
        pass
    return g.ret_success_func(groups=ret)

@GroupView.route('/list/<int:channel_id>', methods=['POST', 'GET'])
def group_by_channel(channel_id):
    channel = Channel.get(channel_id)
    channel_group = [g.id for g in channel.group if g.status]
    # group_list = Group.query.filter_by(status=Group.Status.AVAILABLE).order_by(Group.id.asc()).all()
    ret = []
    for group in channel_group:
        ret.append(orm_obj2dict(group))
    return g.ret_success_func(groups=ret)

@GroupView.route('<int:group_id>', methods=['POST', 'GET'])
def pic_by_group_id(group_id):
    group = Group.get(group_id)
    pics = [pic_build(pic) for pic in group.pics]
    return g.ret_success_func(pics=pics)