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
                            "id": 41,
                            "max": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "min": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "modify_time": "2017-02-17 11:35:45",
                            "normal": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "title": "北包包"
                        },
                        "group_id": "1"
                    },
                    {
                        "pic": {
                            "create_time": "2017-02-17 11:35:45",
                            "id": 41,
                            "max": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "min": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "modify_time": "2017-02-17 11:35:45",
                            "normal": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "title": "北包包"
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
                "category": "the_three",
                "items": [
                    {
                        "pic": {
                            "create_time": "2017-02-17 11:35:45",
                            "id": 41,
                            "max": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "min": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "modify_time": "2017-02-17 11:35:45",
                            "normal": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "title": "北包包"
                        },
                        "group_id": "1",
                        "des": "测试文本"
                    },
                    {
                        "pic": {
                            "create_time": "2017-02-17 11:35:45",
                            "id": 41,
                            "max": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "min": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "modify_time": "2017-02-17 11:35:45",
                            "normal": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "title": "北包包"
                        },
                        "group_id": "1",
                        "des": "测试文本"
                    },
                    {
                        "pic": {
                            "create_time": "2017-02-17 11:35:45",
                            "id": 41,
                            "max": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "min": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "modify_time": "2017-02-17 11:35:45",
                            "normal": "http://test.rs.vogor.cn/image/2017/02/17/6f3e6672bce934d1.jpg",
                            "title": "北包包"
                        },
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

