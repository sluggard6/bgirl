# -*- coding:utf-8 -*-
from flask import Blueprint, request, g
from service.pic_service import pic_build
from bg_biz.orm.page import PageModule

__author__ = [
    'sluggrd'
]

PageView = Blueprint('page', __name__)


@PageView.route('/<page>', methods=['GET', 'POST'])
def page(page):
    return '''
{
    "page": {
        "modules": [
            {
                "category": "banner",
                "items": [
                    {
                        "pic": "",
                        "group_id": "1",
                        "des": "测试文本"
                    }
                ]
            },
            {
                "category": "the_two",
                "items": [
                    {
                        "pic": "",
                        "group_id": "1"
                    },
                    {
                        "pic": "",
                        "group_id": "1"
                    }
                ]
            },
            {
                "category": "title",
                "text": "最优精选"
            },
            {
                "category": "the_two",
                "items": [
                    {
                        "pic": "",
                        "group_id": "1",
                        "des": "测试文本"
                    },
                    {
                        "pic": "",
                        "group_id": "1",
                        "des": "测试文本"
                    }
                ]
            }
        ]
    }
}
    '''

    if page == PageModule.Page.INDEX:
        pass

