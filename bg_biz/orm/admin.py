# -*- coding:utf-8 -*-
"""大本营基础系统"""
import cPickle as pickle
from datetime import datetime

from flask import current_app
from sqlalchemy import *
from sqlalchemy.orm import relation
from werkzeug.utils import cached_property

from bg_biz.signals import admin_rup_changed
from sharper.flaskapp.kvdb import kvdb
from sharper.flaskapp.orm.base import BaseModel, db
from sharper.lib.error import AppError
from sharper.util import helper, string

__authors__ = ['John Chan']

metadata = BaseModel.metadata

_kvdb = kvdb.common

admin_role_permission = Table(u'admin_role_permission', metadata,
							  Column(u'role_id', INTEGER(), ForeignKey('admin_role.id'), primary_key=True,
									 nullable=False),
							  Column(u'permission_id', VARCHAR(length=20), ForeignKey('admin_permission.id'),
									 primary_key=True, nullable=False),
							  )

admin_role_user = Table(u'admin_role_user', metadata,
						Column(u'user_id', INTEGER(), ForeignKey('admin_user.id'), primary_key=True, nullable=False),
						Column(u'role_id', INTEGER(), ForeignKey('admin_role.id'), primary_key=True, nullable=False),
						)


class AdminAction:
	"""
	系统行为 - 需记录log的动作常量
	"""

	SysCreateUser = u'创建系统用户'
	SysUpdateUser = u'更新系统用户'
	SysUpdateUserRole = u'更新系统用户角色'
	SysUpdateUserArea = u'更新系统用户区域'
	SysCreateRole = u'创建系统角色'
	SysUpdateRole = u'更新系统角色'
	SysDelRole = u'删除系统角色'
	SysUpdateRolePermission = u'更新系统角色权限'
	SysCreatePermission = u'创建系统权限'
	SysUpdatePermission = u'更新系统权限'
	SysDelPermission = u'删除系统权限'
	SendPopMessage = u"发送弹窗消息"
	SendSMS = u"发送短信"
	SendNotification = u"发送Notification"
	DelayNetEnd = u"延长上网权限"
	DAFENG_COLLECT = u"达丰统计"


class AdminLog(BaseModel):
	__tablename__ = 'admin_log'

	__table_args__ = {}

	id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
	action = Column(u'action', VARCHAR(length=20), nullable=False)
	user_id = Column(u'user_id', INTEGER())
	key1 = Column(u'key1', VARCHAR(length=50))
	key2 = Column(u'key2', VARCHAR(length=50))
	key3 = Column(u'key3', VARCHAR(length=50))
	data = Column(u'data', TEXT())
	ip = Column(u'ip', CHAR(length=15))
	create_time = Column(u'create_time', TIMESTAMP(timezone=False), nullable=False, default=datetime.now)

	@classmethod
	def load_top_by_user_id(cls, user_id, limit=20):
		return cls.query.filter_by(user_id=user_id).limit(limit).all()

	@classmethod
	def write(cls, action, cuser_id, ip=None, key1=None, key2=None, key3=None, data=None):
		log = AdminLog(action, cuser_id, key1, key2, key3, data, ip)
		log.insert()
		return log

	@property
	def user(self):
		return AdminUser.get(self.user_id)


class AdminPermission(BaseModel):
	__tablename__ = 'admin_permission'

	__table_args__ = {}

	id = Column(u'id', VARCHAR(length=20), primary_key=True, nullable=False, autoincrement=False)
	parent_id = Column(u'parent_id', VARCHAR(length=20), nullable=False)
	name = Column(u'name', VARCHAR(length=50), nullable=False)
	key = Column(u'key', VARCHAR(length=50), nullable=False)
	path = Column(u'path', VARCHAR(length=200))
	description = Column(u'description', VARCHAR(length=200))
	status = Column(u'status', Integer(), nullable=False, default=1)

	admin_roles = relation('AdminRole',
						   primaryjoin='AdminPermission.id==admin_role_permission.c.permission_id',
						   secondary=admin_role_permission,
						   secondaryjoin='admin_role_permission.c.role_id==AdminRole.id')

	def _after_update(self):
		admin_rup_changed.send(self)

	_after_delete = _after_update

	def _before_update(self):
		"""
		禁止修改、删除基本权限 - 例如基础权限管理系统
		@return:
		"""

	_before_delete = _before_update


class AdminRole(BaseModel):
	__tablename__ = 'admin_role'

	__table_args__ = {}

	id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
	name = Column(u'name', VARCHAR(length=25), nullable=False)
	description = Column(u'description', VARCHAR(length=200))
	status = Column(u'status', Integer(), nullable=False, default=1)

	admin_permissions = relation('AdminPermission',
								 primaryjoin='AdminRole.id==admin_role_permission.c.role_id',
								 secondary=admin_role_permission,
								 secondaryjoin='admin_role_permission.c.permission_id==AdminPermission.id')

	admin_users = relation('AdminUser',
						   primaryjoin='AdminRole.id==admin_role_user.c.role_id',
						   secondary=admin_role_user,
						   secondaryjoin='admin_role_user.c.user_id==AdminUser.id')

	def _before_update(self):
		if self.name == 'admin':
			raise AppError(u'该角色不能编辑、删除！')

	_before_delete = _before_update

	def _clear_all_permissions(self):
		db.engine.execute('DELETE FROM admin_role_permission WHERE role_id=%s', self.id)

	def update_permissions(self, permission_id_list):
		"""
		批量更新权限到角色
		@param permission_id_list: 权限id列表
		@return:
		"""
		self._clear_all_permissions()
		if permission_id_list:
			db.engine.execute(admin_role_permission.insert(), [
				dict(role_id=self.id, permission_id=pid) for pid in permission_id_list
				])
		admin_rup_changed.send(self)

	@cached_property
	def permission_count(self):
		return len(self.admin_permissions)


class AdminUser(BaseModel):
	__tablename__ = 'admin_user'

	__table_args__ = {}

	id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
	user_name = Column(u'user_name', VARCHAR(length=45), nullable=False)
	password = Column(u'password', VARCHAR(length=50), nullable=False)
	description = Column(u'description', VARCHAR(length=50), nullable=True)
	status = Column(u'status', Integer(), nullable=False, default=1)
	create_time = Column(u'create_time', DATETIME(timezone=False), nullable=False)

	admin_roles = relation('AdminRole',
						   primaryjoin='AdminUser.id==admin_role_user.c.user_id',
						   secondary=admin_role_user,
						   secondaryjoin='admin_role_user.c.role_id==AdminRole.id')

	@cached_property
	def admin_areas(self):

		return [int(row[0]) for row in
				db.get_engine(current_app).execute("SELECT * FROM admin_area WHERE user_id=" + str(self.id))]

	@classmethod
	def get_by_name(cls, user_name):
		return cls.query.filter_by(user_name=user_name).first()
# 		try:
# 			return cls.query.filter_by(user_name=user_name).first()
# 		except:
# 			return None

	def check_password(self, pwd):
		return self.password == string.md5(pwd)

	@classmethod
	def get_password(cls, pwd):
		return string.md5(pwd)

	def gen_password(self, pwd):
		self.password = string.md5(pwd)

	@cached_property
	def all_permissions_key(self):
		return 'admin_user:permission:%s' % self.id

	@cached_property
	def all_permissions(self):
		"""
		获取用户的所有权限
		@return:
		"""
		key = self.all_permissions_key
		pm_list = []

		if not pm_list:
			for r in self.admin_roles:
				if r.status:
					for p in r.admin_permissions:
						if p.status: pm_list.append(p)
			_kvdb.setex(key, pickle.dumps(pm_list), helper.good_cache_time('7d'))
		else:
			pm_list = pickle.loads(pm_list)
		return sorted(set(pm_list), key=lambda x: x.id)

	@cached_property
	def all_role_names(self):
		"""
		获取用户的所有角色名
		@return:
		"""
		return [r.name for r in self.admin_roles]

	def has_role(self, role_name):
		return role_name in self.all_role_names

	def has_permissions(self, p_keys):
		return filter(lambda p: p.key in p_keys, self.all_permissions)

	def clear_permissions(self):
		_kvdb.delete(self.all_permissions_key)

	@staticmethod
	def clear_all_user_permissions_cache(obj):
		"""
		移除所有用户权限缓存
		@return:
		"""
		_kvdb.delete(*_kvdb.keys('admin_user:permission:*'))

	@cached_property
	def top_permissions(self):
		"""
		获取用户顶级权限 - 显示在top bar
		@return:
		"""
		return [p for p in self.all_permissions if p.parent_id == '0']

	def sub_permissions(self, parant_id):
		"""
		获取指定权限的直接子权限
		@param parant_id:
		@return:
		"""
		return [p for p in self.all_permissions if p.parent_id == parant_id]

	def sub_permissions_all(self, parant_id):
		"""
		获取指定权限的全部子权限
		@param parant_id:
		@return:
		"""
		return [p for p in self.all_permissions if p.parent_id.startswith(parant_id)]

	def get_permission_by_key(self, key):
		"""
		获取指定key的权限
		@param key:
		@return:
		"""
		for p in self.all_permissions:
			if p.key == key:
				return p

	def _clear_all_roles(self):
		db.engine.execute('DELETE FROM admin_role_user WHERE user_id=%s', self.id)

	def _clear_all_areas(self):
		db.engine.execute('DELETE FROM admin_area WHERE user_id=%s', self.id)

	def update_roles(self, role_id_list):
		"""
		批量更新角色到用户
		@param role_id_list: 角色id列表
		@return:
		"""
		self._clear_all_roles()
		if role_id_list:
			db.engine.execute(admin_role_user.insert(), [
				dict(user_id=self.id, role_id=rid) for rid in role_id_list
				])
		admin_rup_changed.send(self)

	def update_areas(self, area_id_list):
		self._clear_all_areas()
		for area_id in area_id_list:
			db.engine.execute("insert into admin_area values (%s,%s)" % (area_id, self.id))

	def add_role(self, role_id):
		db.engine.execute(admin_role_user.insert(), (self.id, role_id))


class AdminArea(BaseModel):
	__tablename__ = 'admin_area'

	__table_args__ = {}

	id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
	user_id = Column(u'user_id', INTEGER(), nullable=False)
	area_id = Column(u'area_id', INTEGER(), nullable=False)
	create_time = Column(u'create_time', DATETIME(timezone=False), nullable=False)

	@classmethod
	def get_admin_areas(cls, user_id):
		areas = cls.query.filter_by(user_id=user_id).all()
		area_id_list = []
		for area in areas:
			area_id_list.append(area.area_id)
		return area_id_list
