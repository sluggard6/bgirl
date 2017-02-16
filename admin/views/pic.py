# -*- coding:utf-8 -*-
from flask import Blueprint, render_template
from bg_biz.orm.pic import Pic

__authors__ = [
    'sluggard'
]


PicView = Blueprint('pic', __name__)


@PicView.route('/all', methods=['POST', 'GET'])
def all_pic():
    pics = Pic.query.all()
    
    return render_template('pic/list.html', pics=pics)