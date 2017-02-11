# -*- coding:utf-8 -*-
"""权限管理"""
from flask import (g, render_template, Blueprint, flash, request, redirect, url_for)
from sqlalchemy.exc import IntegrityError

from form.manage import AdminUserForm, AdminRoleForm, AdminPermissionForm
from bg_biz.orm.admin import AdminUser, AdminRole, AdminPermission, AdminAction, AdminLog
from sharper.flaskapp.orm.base import db

__authors__ = [
	'"linnchord gao" <linnchord@gmail.com>'
]

ManageView = Blueprint('sys_manage', __name__)


@ManageView.route('/user', methods=['GET', 'POST'])
# @permission('sys_user')
def user_manage():
	user_list = AdminUser.query.order_by(AdminUser.id.asc()).all()

	# 除admin自己其他用户不能操作admin
	if g.me.user_name != 'admin':
		user_list = filter(lambda u: u.user_name != 'admin', user_list)
	return render_template('manage/user.html', user_list=user_list)


@ManageView.route('/user/new', methods=['GET', 'POST'])
@ManageView.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
# @permission('sys_user')
def user_edit(user_id=None):
	form = AdminUserForm()

	if user_id:
		cuser = AdminUser.get(user_id)
		act = u'编辑'
		if request.method == 'GET':
			form.user_name.data = cuser.user_name
			form.status.data = cuser.status
			form.description.data = cuser.description
		form.user_name.flags.disabled = u'disabled'
	else:
		cuser = None
		act = u'创建'

	if request.method == 'POST':
		if form.validate_on_submit():
			if not cuser:
				user_name = form.user_name.data.strip()
				password = form.password.data.strip()
				description = form.description.data.strip()
				if not user_name:
					form.user_name.errors = [u'请输入用户名！']
				elif not password:
					form.password.errors = [u'请输入密码']
				else:
					try:
						cuser = AdminUser(
							user_name,
							AdminUser.get_password(password),
							description
						).insert()
						AdminLog.write(AdminAction.SysCreateUser, g.me.id, ip=request.remote_addr, key1=cuser.id,
									   key2=cuser.user_name)
						flash(u'创建用户成功', 'ok')
					except IntegrityError as e:
						print e
						db.session.rollback()
						form.user_name.errors = [u'用户名重复！']
			else:
				try:
					if form.password.data:
						cuser.gen_password(form.password.data.strip())
					cuser.status = 1 if form.status.data else 0
					cuser.description = form.description.data
					cuser.update()
					AdminLog.write(AdminAction.SysUpdateUser, g.me.id, ip=request.remote_addr, key1=cuser.id,
								   key2=cuser.user_name)

					form.user_name.data = cuser.user_name
					flash(u'修改用户成功', 'ok')
				except IntegrityError as e:
					db.session.rollback()
					form.user_name.errors = [u'用户名重复！']

	return render_template('manage/user_edit.html', act=act, cuser=cuser, form=form)


@ManageView.route('/user/<int:user_id>/roles', methods=['GET', 'POST'])
# @permission('sys_user')
def user_roles_manage(user_id):
	cuser = AdminUser.get(user_id)

	if request.method == 'POST':
		r_list = request.form.getlist('role_selected')
		cuser.update_roles(map(lambda x: int(x), r_list))
		AdminLog.write(AdminAction.SysUpdateUserRole, g.me.id, ip=request.remote_addr, key1=user_id, data=str(r_list))

		flash(u'更新成功', 'ok')
		return redirect(url_for('.user_roles_manage', user_id=user_id))

	cuser_roles = [r.id for r in cuser.admin_roles if r.status]
	role_list = AdminRole.query.filter_by(status=1).order_by(AdminRole.id.desc()).all()

	# 当用户不是admin时不能关联admin角色
	if g.me.user_name == 'admin':
		g.is_admin = True
	# if g.me.user_name != 'admin':

	#    role_list = filter(lambda r: r.name != 'admin', role_list)

	return render_template('manage/user_roles.html', cuser_roles=cuser_roles, role_list=role_list, cuser=cuser)


@ManageView.route('/role', methods=['GET', 'POST'])
# @permission('sys_role')
def role_manage():
	role_list = AdminRole.query.order_by(AdminRole.id.desc()).all()
	# 当用户不是admin时不能设置admin角色
	if g.me.user_name != 'admin':
		role_list = filter(lambda r: r.name != 'admin', role_list)
	return render_template('manage/role.html', role_list=role_list)


@ManageView.route('/role/<int:role_id>/del', methods=['GET'])
# @permission('sys_role')
def role_del(role_id):
	role = AdminRole.get(role_id)
	jsn = role.to_json()
	role.delete()
	AdminLog.write(AdminAction.SysDelRole, g.me.id, ip=request.remote_addr, data=jsn)
	flash(u'已移除指定角色', 'ok')
	return redirect('/manage/role')


@ManageView.route('/role/new', methods=['GET', 'POST'])
@ManageView.route('/role/<int:role_id>/edit', methods=['GET', 'POST'])
# @permission('sys_role')
def role_edit(role_id=None):
	form = AdminRoleForm()

	if role_id:
		role = AdminRole.get(role_id)
		act = u'编辑'
		if request.method == 'GET':
			form.name.data = role.name
			form.description.data = role.description
			form.status.data = role.status
	else:
		role = None
		act = u'创建'

	if request.method == 'POST':
		if form.validate_on_submit():
			if not role:
				name = form.name.data.strip()
				if not name:
					form.name.errors = [u'请输入角色名！']
				else:
					try:
						role = AdminRole(
							name,
							form.description.data.strip()
						).insert()
						AdminLog.write(AdminAction.SysCreateRole, g.me.id, ip=request.remote_addr, key1=role.id,
									   key2=role.name)
						flash(u'创建角色成功', 'ok')
					except IntegrityError:
						db.session.rollback()
						form.name.errors = [u'角色名重复！']
			else:
				try:
					role.name = form.name.data.strip()
					role.description = form.description.data.strip()
					role.status = 1 if form.status.data else 0
					role.update()

					AdminLog.write(AdminAction.SysUpdateRole, g.me.id, ip=request.remote_addr, key1=role.id,
								   key2=role.name)

					form.name.data = role.name
					flash(u'修改角色成功', 'ok')
				except IntegrityError:
					db.session.rollback()
					form.name.errors = [u'角色名重复！']

	return render_template('manage/role_edit.html', act=act, role=role, form=form)


@ManageView.route('/role/<int:role_id>/permissions', methods=['GET', 'POST'])
# @permission('sys_role')
def role_permissions_manage(role_id):
	role = AdminRole.get(role_id)

	if request.method == 'POST':
		p_list = request.form.getlist('permission_selected')
		role.update_permissions(p_list)

		AdminLog.write(AdminAction.SysUpdateRolePermission, g.me.id, ip=request.remote_addr, key1=role.id,
					   key2=role.name, data=str(p_list))

		flash(u'更新成功', 'ok')
		return redirect(url_for('.role_permissions_manage', role_id=role_id))

	role_permissions = [p.id for p in role.admin_permissions if p.status]
	permission_list = AdminPermission.query.filter_by(status=1).order_by(AdminPermission.id.asc()).all()

	return render_template(
		'manage/role_permissions.html', role=role,
		role_permissions=role_permissions, permission_list=permission_list)


@ManageView.route('/permission', methods=['GET', 'POST'])
# @permission('sys_permission')
def permission_manage():
	permission_list = AdminPermission.query.order_by(AdminPermission.id.asc()).all()
	return render_template('manage/permission.html', permission_list=permission_list)


@ManageView.route('/permission/<int:p_id>/del', methods=['GET'])
# @permission('sys_permission')
def permission_del(p_id):
	permn = AdminPermission.get(p_id)
	name = permn.name
	jsn = permn.to_json()
	permn.delete()
	AdminLog.write(AdminAction.SysDelPermission, g.me.id, ip=request.remote_addr, key1=p_id, key3=name, data=jsn)
	flash(u'已移除指定权限', 'ok')
	return redirect('/manage/permission')


@ManageView.route('/permission/new', methods=['GET', 'POST'])
@ManageView.route('/permission/<int:p_id>/edit', methods=['GET', 'POST'])
# @permission('sys_permission')
def permission_edit(p_id=None):
	form = AdminPermissionForm()

	if p_id:
		permission = AdminPermission.get(p_id)
		act = u'编辑'
		if request.method == 'GET':
			form.id.data = permission.id
			form.parent_id.data = permission.parent_id
			form.name.data = permission.name
			form.key.data = permission.key
			form.path.data = permission.path
			form.description.data = permission.description
			form.status.data = permission.status
	else:
		permission = None
		act = u'创建'

	if request.method == 'POST':
		if form.validate_on_submit():
			if not permission:
				try:
					permission = AdminPermission(
						form.id.data.strip(),
						form.parent_id.data.strip(),
						form.name.data.strip(),
						form.key.data.strip(),
						form.path.data.strip(),
						form.description.data.strip()
					).insert()
					AdminLog.write(AdminAction.SysCreatePermission, g.me.id, ip=request.remote_addr, key1=permission.id,
								   key2=permission.name)
					flash(u'创建权限成功', 'ok')
				except IntegrityError:
					db.session.rollback()
					print "记录重复"
					flash(u'存在重复记录，id/parent_id/权限名/key，请检查！', 'warning')
			else:
				try:
					permission.id = form.id.data.strip()
					permission.parent_id = form.parent_id.data.strip()
					permission.name = form.name.data.strip()
					permission.key = form.key.data.strip()
					permission.path = form.path.data.strip()
					permission.description = form.description.data.strip()
					permission.status = 1 if form.status.data else 0
					permission.update()
					AdminLog.write(AdminAction.SysUpdatePermission, g.me.id, ip=request.remote_addr, key1=permission.id,
								   key2=permission.name)
					flash(u'修改权限成功', 'ok')
				except IntegrityError:
					db.session.rollback()
					flash(u'存在重复记录，id/parent_id/权限名/key，请检查！', 'warning')

	return render_template('manage/permission_edit.html', act=act, permission=permission, form=form)


@ManageView.route('/log', methods=['GET'])
# @permission('sys_log')
def log_manager():
	logs = AdminLog.query.order_by(AdminLog.id.desc()).limit(200).all()
	for l in logs: l.cuser = AdminUser.get(l.user_id)
	return render_template('manage/log.html', logs=logs)
