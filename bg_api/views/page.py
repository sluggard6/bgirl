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
                        "pic": {
                            "create_time": "2017-02-17 11:35:45",
                            "id": 45,
                            "max": "http://rs.vogor.cn/image/2017/02/17/1908bf2a109063e8.jpg",
                            "min": "http://rs.vogor.cn/image/2017/02/17/1908bf2a109063e8.jpg",
                            "modify_time": "2017-02-17 11:35:45",
                            "normal": "http://rs.vogor.cn/image/2017/02/17/1908bf2a109063e8.jpg",
                            "title": "111"
                        },
                        "group_id": "1"
                    },
                    {
                        "pic": {
                            "create_time": "2017-02-17 11:35:45",
                            "id": 45,
                            "max": "http://rs.vogor.cn/image/2017/02/17/1908bf2a109063e8.jpg",
                            "min": "http://rs.vogor.cn/image/2017/02/17/1908bf2a109063e8.jpg",
                            "modify_time": "2017-02-17 11:35:45",
                            "normal": "http://rs.vogor.cn/image/2017/02/17/1908bf2a109063e8.jpg",
                            "title": "111"
                        },
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

