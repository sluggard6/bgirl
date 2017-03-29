# -*- coding:utf-8 -*-
from bg_biz.orm.pic import Group, Channel
from flask import Blueprint, g, request
from bg_biz.service.pic_service import pic_build, group_build
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
    groups = [group_build(gu) for gu in channel.group]
    return g.ret_success_func(groups=groups)

@GroupView.route('/<int:group_id>', methods=['POST', 'GET'])
def pic_by_group_id(group_id):
    group = Group.get(group_id)
    pics = [pic_build(pic) for pic in group.pics]
    return g.ret_success_func(pics=pics, group=orm_obj2dict(group))