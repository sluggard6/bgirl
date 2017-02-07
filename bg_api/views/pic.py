# -*- coding:utf-8 -*-
from bg_biz.orm.pic import Pic
from flask import Blueprint, request, g
from service.pic_service import pic_build

__author__ = [
    'sluggrd'
]

PicView = Blueprint('pic', __name__)


@PicView.route('/list', methods=['POST', 'GET'])
def list():
    data = request.args or request.form
    _ids = data.get('ids')
    pics = Pic.query.filter(Pic.id.in_(_ids)).all()
    ret = []
    for pic in pics:
        ret.append(pic_build(pic))
    return g.ret_success_func(pics=ret)

@PicView.route('/<int:id>', methods=['POST', 'GET'])
def one(id):
    pic = Pic.get_by_kvdb(id)
    return g.ret_success_func(pic=pic_build(pic))