# -*- coding:utf-8 -*-

from flask import (g, render_template, Blueprint, flash, request, redirect, url_for, jsonify)
from sqlalchemy.exc import IntegrityError
from bg_biz.orm.pic import Supplier
from form.channel import SupplierForm
from form import obj2form, form2obj
from sharper.flaskapp.orm.base import db
from bg_biz.orm.admin import AdminLog, AdminAction

__authors__ = [
    'John Chan'
]

SupplierView = Blueprint('supplier', __name__)


@SupplierView.route('/list', methods=['GET', 'POST'])
def list():
    supplier = Supplier.query.filter(Supplier.status<>3).all()
    return render_template('supplier/list.html', suppliers=supplier)


@SupplierView.route('/delete', methods=['GET', 'POST'])
def delete():
    data = request.form or request.args
    print data
    id = data.get('id', None)
    supplier = Supplier.query.filter_by(id=id).first()
    supplier.status = 3
    supplier.update()
    flash(u'删除成功', 'ok')
    return redirect(url_for("supplier.list"))


@SupplierView.route('/edit', methods=['GET', 'POST'])
def edit():
    data = request.form or request.args
    print data
    id = data.get('id', None)
    form = SupplierForm()
    print 'Supplier=', id

    if id:
        supplier = Supplier.get(id)
        act = u'编辑'
        if request.method == 'GET':
            obj2form(supplier, form)
        form.name.flags.disabled = u'disabled'
    else:
        supplier = None
        act = u'创建'

    if request.method == 'POST':
        if form.validate_on_submit():
            if not supplier:
                form = SupplierForm(request.form)
                supplier = Supplier()
                form2obj(form, supplier)
                try:
                    supplier.id = None
                    supplier.insert()
                    AdminLog.write("添加供应商", g.me.id, ip=request.remote_addr, key1=supplier.id,
                                   key2=supplier.name)
                    flash(u'创建频道成功', 'ok')
                    return redirect(url_for("supplier.list"))
                except IntegrityError as e:
                    print e
                    db.session.rollback()
                    form.user_name.errors = [u'频道名重复！']
            else:
                try:
                    supplier.status = 1 if form.status.data else 0
                    supplier.description = form.description.data
                    supplier.update()
                    AdminLog.write("修改频道", g.me.id, ip=request.remote_addr, key1=supplier.id,
                                   key2=supplier.name)

                    form.name.data = supplier.name
                    flash(u'修改频道成功', 'ok')
                    return redirect(url_for("supplier.list"))
                except IntegrityError as e:
                    db.session.rollback()
                    form.user_name.errors = [u'频道名重复！']

    return render_template('supplier/edit.html', act=act, supplier=supplier, form=form)
