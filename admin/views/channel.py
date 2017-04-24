# -*- coding:utf-8 -*-

from flask import (g, render_template, Blueprint, flash, request, redirect, url_for, jsonify)
from sqlalchemy.exc import IntegrityError
from bg_biz.orm.pic import Channel, Group, Pic, Supplier
from form.channel import ChannelForm, GroupForm
from form import obj2form, form2obj
from sharper.flaskapp.orm.base import db
from bg_biz.orm.admin import AdminLog, AdminAction

__authors__ = [
    'John Chan'
]

ChannelView = Blueprint('channel', __name__)


@ChannelView.route('/list', methods=['GET', 'POST'])
def list():
    channels = Channel.query.filter(Channel.status <> 3).order_by(Channel.id.asc()).all()

    return render_template('channel/list.html', channels=channels)


@ChannelView.route('/channel_delete', methods=['GET', 'POST'])
def channel_delete():
    data = request.form or request.args
    print data
    id = data.get('id', None)
    channel = Channel.query.filter_by(id=id).first()
    channel.status = 3
    channel.update()
    flash(u'删除成功', 'ok')
    return redirect(url_for("channel.list"))


@ChannelView.route('/edit', methods=['GET', 'POST'])
def edit():
    data = request.form or request.args
    print data
    id = data.get('id', None)
    form = ChannelForm()
    print 'channel=', id

    if id:
        channel = Channel.get(id)
        act = u'编辑'
        if request.method == 'GET':
            obj2form(channel, form)
        form.name.flags.disabled = u'disabled'
    else:
        channel = None
        act = u'创建'

    if request.method == 'POST':
        if form.validate_on_submit():
            if not channel:
                form = ChannelForm(request.form)
                channel = Channel()
                form2obj(form, channel)
                try:
                    channel.id = None
                    channel.insert()
                    AdminLog.write("添加频道", g.me.id, ip=request.remote_addr, key1=channel.id,
                                   key2=channel.name)
                    flash(u'创建频道成功', 'ok')
                    return redirect(url_for("channel.list"))
                except IntegrityError as e:
                    print e
                    db.session.rollback()
                    form.user_name.errors = [u'频道名重复！']
            else:
                try:
                    channel.status = 1 if form.status.data else 0
                    channel.description = form.description.data
                    channel.update()
                    AdminLog.write("修改频道", g.me.id, ip=request.remote_addr, key1=channel.id,
                                   key2=channel.name)

                    form.name.data = channel.name
                    flash(u'修改频道成功', 'ok')
                    return redirect(url_for("channel.list"))
                except IntegrityError as e:
                    db.session.rollback()
                    form.user_name.errors = [u'频道名重复！']

    return render_template('channel/edit.html', act=act, channel=channel, form=form)


@ChannelView.route('/group/<int:channel_id>', methods=['GET', 'POST'])
def group(channel_id):
    channel = Channel.get(channel_id)

    if request.method == 'POST':
        r_list = request.form.getlist('group_selected')
        channel.update_groups(map(lambda x: int(x), r_list))
        AdminLog.write("更新", g.me.id, ip=request.remote_addr, key1=channel_id, data=str(r_list))

        flash(u'更新成功', 'ok')
        return redirect(url_for('.group', channel_id=channel_id))

    channel_group = [r.id for r in channel.group if r.status]
    groups = Group.query.filter_by(status=1).order_by(Group.id.desc()).all()

    return render_template('channel/groups.html', channel_group=channel_group, groups=groups, channel=channel)


@ChannelView.route('/group_list', methods=['GET', 'POST'])
def group_list():
    data = request.form or request.args
    supplier_id = data.get('supplier_id',0)
    name = data.get('name', None)
    suppliers = Supplier.query.filter(Supplier.status<>3).all()
    g.suppliers = suppliers
    g.supplier_id = supplier_id
    base_query = Group.query.filter(Group.status <> 3).order_by(Group.id.asc())
    if supplier_id and str(supplier_id) != '0':
        print supplier_id
        base_query = base_query.filter_by(supplier_id=supplier_id)
    if name:
        print '==',name,'--'
        base_query = base_query.filter(Group.name.like("%"+name+"%"))
    groups = base_query.all()
    return render_template('channel/group_list.html', groups=groups)


@ChannelView.route('/group_edit', methods=['GET', 'POST'])
def group_edit():
    data = request.form or request.args
    print data
    id = data.get('id', None)
    suppliers = Supplier.query.filter_by(status=1).order_by(Supplier.id.asc()).all()
    g.suppliers = suppliers
    form = GroupForm()
    print 'channel=', id
    channels = Channel.query.filter_by(status=1).order_by(Channel.id.asc()).all()
    g.channels = channels
    if id:
        group = Group.get(id)
        g.thumb = group.thumb_http
        g.thumb2 = group.thumb2_http
        g.thumb3 = group.thumb3_http
        g.thumb4 = group.thumb4_http
        g.photo_and_thumbs = group.pics
        g.supplier_id = group.supplier_id
        act = u'编辑'
        if request.method == 'GET':
            obj2form(group, form)
        form.name.flags.disabled = u'disabled'
    else:
        group = None
        g.supplier_id = 0
        act = u'创建'

    if request.method == 'POST':
        if form.validate_on_submit():
            if not group:
                form = GroupForm(request.form)
                group = Group()
                form2obj(form, group)
                try:
                    group.id = None
                    group.insert()
                    if form.images.data:
                        images = form.images.data.split(';')
                        img_list = []
                        for img in images:
                            pic = Pic()
                            pic.title = group.name
                            pic.max = img;
                            pic.normal = img;
                            pic.min = img
                            pic.good = 0
                            pic.bad = 0
                            pic.insert()
                            img_list.append(pic.id)
                        group.update_pics(img_list);
                    AdminLog.write("新组添加", g.me.id, ip=request.remote_addr, key1=group.id,
                                   key2=group.name)
                    flash(u'创建组成功', 'ok')
                    r_list = request.form.getlist('channel_selected')
                    group.update_channels(map(lambda x: int(x), r_list))
                    return redirect(url_for("channel.group_list"))
                except IntegrityError as e:
                    print e
                    db.session.rollback()
                    form.user_name.errors = [u'组名重复！']
            else:
                try:

                    group.thumb = form.thumb.data
                    group.thumb2 = form.thumb2.data
                    group.thumb3 = form.thumb3.data
                    group.thumb4 = form.thumb4.data
                    group.status = 1 if form.status.data else 0
                    group.description = form.description.data
                    group.supplier_id = form.supplier_id.data
                    group.group_no = form.group_no.data
                    group.shoot_time = form.shoot_time.data
                    group.name = form.name.data
                    group.update()
                    img_list = []
                    if form.images.data:
                        images = form.images.data.split(';')
                        for img in images:
                            pic = Pic()
                            pic.title = group.name
                            pic.max = img;
                            pic.normal = img;
                            pic.min = img
                            pic.good = 0
                            pic.bad = 0
                            pic.insert()
                            img_list.append(pic.id)
                    group.update_pics(img_list);
                    AdminLog.write("修改组", g.me.id, ip=request.remote_addr, key1=group.id,
                                   key2=group.name)

                    form.name.data = group.name
                    flash(u'修改组成功', 'ok')
                    r_list = request.form.getlist('channel_selected')
                    group.update_channels(map(lambda x: int(x), r_list))
                    return redirect(url_for("channel.group_list"))
                except IntegrityError as e:
                    db.session.rollback()
                    form.user_name.errors = [u'组名重复！']

    return render_template('channel/group_edit.html', act=act, group=group, form=form)


@ChannelView.route('/group_delete', methods=['GET', 'POST'])
def group_delete():
    data = request.form or request.args
    print data
    id = data.get('id', None)
    group = Group.query.filter_by(id=id).first()
    group.status = 3
    group.update()
    flash(u'删除成功', 'ok')
    return redirect(url_for("channel.group_list"))


@ChannelView.route('/create_pic', methods=['GET', 'POST'])
def create_pic():
    data = request.form or request.args
    uri = data.get('uri', None)
    group_name = data.get('group_name', None)
    pic = Pic()
    pic.title = u'封面'
    pic.max = uri;
    pic.normal = uri;
    pic.min = uri
    pic.good = 0
    pic.bad = 0
    pic.insert()
    return jsonify(success=True, pic_id=pic.id)


# @ChannelView.route('/test', methods=['GET', 'POST'])
# def test():
#     for i in range(23, 69):
#         group = Group.query.filter_by(id=i).first()
#         if group:
#             if group.thumb:
#                 pic = Pic()
#                 pic.title = u''
#                 pic.max = group.thumb
#                 pic.normal = group.thumb
#                 pic.min = group.thumb
#                 pic.good = 0
#                 pic.bad = 0
#                 pic.insert()
#                 group.thumb = pic.id
#                 group.update()
#             if group.thumb2:
#                 pic = Pic()
#                 pic.title = u''
#                 pic.max = group.thumb2
#                 pic.normal = group.thumb2
#                 pic.min = group.thumb2
#                 pic.good = 0
#                 pic.bad = 0
#                 pic.insert()
#                 group.thumb2 = pic.id
#                 group.update()
#             if group.thumb3:
#                 pic = Pic()
#                 pic.title = u''
#                 pic.max = group.thumb3
#                 pic.normal = group.thumb3
#                 pic.min = group.thumb3
#                 pic.good = 0
#                 pic.bad = 0
#                 pic.insert()
#                 group.thumb3 = pic.id
#                 group.update()
#     return jsonify(success=True)