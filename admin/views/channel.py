# -*- coding:utf-8 -*-

from flask import (g, render_template, Blueprint, flash, request, redirect, url_for)
from sqlalchemy.exc import IntegrityError
from bg_biz.orm.pic import Channel, Group, Pic
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
    channels = Channel.query.order_by(Channel.id.asc()).all()

    return render_template('channel/list.html', channels=channels)


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
    groups = Group.query.order_by(Group.id.asc()).all()

    return render_template('channel/group_list.html', groups=groups)


@ChannelView.route('/group_edit', methods=['GET', 'POST'])
def group_edit():
    data = request.form or request.args
    print data
    id = data.get('id', None)

    form = GroupForm()
    print 'channel=', id
    channels = Channel.query.filter_by(status=1).order_by(Channel.id.asc()).all()
    g.channels = channels
    if id:
        group = Group.get(id)
        g.thumb =group.thumb_http
        g.thumb2 = group.thumb2_http
        g.thumb3 = group.thumb3_http
        g.photo_and_thumbs = group.pics
        act = u'编辑'
        if request.method == 'GET':
            obj2form(group, form)
        form.name.flags.disabled = u'disabled'
    else:
        group = None
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
                    group.status = 1 if form.status.data else 0
                    group.description = form.description.data

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
