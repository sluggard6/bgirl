# -*- coding:utf-8 -*-
from flask import Blueprint, request, g, render_template
from bg_biz.service.pic_service import pic_build
from bg_biz.orm.page import PageModule, PageContent

__author__ = [
    'sluggrd'
]

PageView = Blueprint('page', __name__)


@PageView.route('/<page>', methods=['GET', 'POST'])
def page(page):
    ms = PageModule.query.filter_by(page=page).filter_by(status=PageModule.Status.AVAILABLE).order_by(PageModule.rank.desc()).order_by(PageModule.id).all()
    mds = [m.id for m in ms]
    ccs = PageContent.query.filter(PageContent.module_id.in_(mds)).all()
    mc = dict()
    for pc in ccs:
        if pc.module_id in mc:
            cs = mc[pc.module_id]
        else:
            cs = []
        cs.append(pc)
        mc[pc.module_id]=cs
    return render_template("page.json", ms=ms, mc=mc)


    '''
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