# -*- coding:utf-8 -*-

__author__ = [
    "sluggrd"
]

def pic_build(pic):
    dic = dict()
    dic['id'] = pic.id
    dic['title'] = pic.title
    dic['min'] = pic.d_min
    dic['normal'] = pic.d_normal
    dic['max'] = pic.d_max
    dic['create_time'] = pic.create_time.strftime("%Y-%m-%d %H:%M:%S")
    dic['modify_time'] = pic.modify_time.strftime("%Y-%m-%d %H:%M:%S")
    return dic


def group_build(group):
    dic = dict()
    dic['id'] = group.id
    dic['name'] = group.name
    dic['description'] = group.description
    dic['status'] = group.status
    dic['t1'] = group.thumb_http
    dic['t2'] = group.thumb2_http
    dic['t3'] = group.thumb3_http
    dic['t4'] = group.thumb4_http
    return dic
    
