# -*- coding:utf-8 -*-
from sharper.flaskapp.kvdb import kvdb
from sharper.flaskapp.orm.base import BaseModel, db
from sharper.flaskapp.orm.display_enum import DisplayEnum
from sharper.flaskapp.orm.kvdb_mixin import KvdbMixin
from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, Table, ForeignKey

from bg_biz.utils import get_download_url

from datetime import datetime

from pic import Pic
from bg_biz.orm.pic import Group


class PageModule(BaseModel):
    __tablename__ = 'page_module'
    __table_args__ = {}

    class Status(DisplayEnum):
        AVAILABLE = 1
        DISABLE = 0

        __display_cn__ = {
            AVAILABLE: u'有效',
            DISABLE: u'无效'
        }
        
    class Page(DisplayEnum):
        INDEX = "index"
        GERENGUAN = "gerenguan"
        PINPAIGUAN = "pinpaiguan"
        ZHUTIGUAN = "zhutiguan"
        
        __display_cn__ = {
            INDEX: u"首页",
            GERENGUAN: u"个人馆",
            PINPAIGUAN: u"品牌馆",
            ZHUTIGUAN: u"主题馆"
        }
    
    class Category(DisplayEnum):
        TITLE = "title"
        BANNER = "banner"
        TEH_TWO = "the_two"
        THE_THREE = "the_three"
        THREE_CIRCLE = "three_circle"
        
        __display_cn__ = {
            TITLE: u"标题",
            BANNER: u"大图",
            TEH_TWO: u"左右两张",
            THE_THREE: u"三张方形",
            THREE_CIRCLE: u"三张圆形",
        }
    
    
    id = Column(u'id', INTEGER(), nullable=False,primary_key=True,autoincrement=True)
    page = Column(u'page', VARCHAR(length=20), nullable=False)
    category = Column(u'category', VARCHAR(length=20), nullable=False,default=1)
    text = Column(u'text', VARCHAR(length=50), nullable=True)
    icon = Column(u'icon', VARCHAR(length=200), nullable=True)
    des = Column(u'des', VARCHAR(length=500), nullable=True)
    style = Column(u'style', None, nullable=True)
    extend = Column(u'extend', None, nullable=True)
    rank = Column(u'rank', INTEGER(), nullable=False,default=0)
    status = Column(u'status', INTEGER(), nullable=False,default=0)
    createtime = Column(u'createtime', DATETIME(), nullable=False,default=datetime.now())
    modifytime = Column(u'modifytime', DATETIME(), nullable=False,default=datetime.now())
    createby = Column(u'createby', VARCHAR(length=50), nullable=True)
    modifyby = Column(u'modifyby', VARCHAR(length=50), nullable=True)

    @property
    def content_pics(self):
        pics = []
        base = PageContent.query.filter_by(module_id=self.id).filter_by(status=1)
        if self.category == PageModule.Category.BANNER:
            content = base.limit(1).all()
            l = len(content)
            s = 1-l
            for c in content:
                cc = dict(id=c.id,pic=c.pic.d_min)
                pics.append(cc)
            for i in range(s):
                cc = dict(id=0, pic=get_download_url('image', 'no_pic.jpg'))
                pics.append(cc)
        elif self.category == PageModule.Category.TEH_TWO:
            content = base.limit(2).all()
            l = len(content)
            s = 2-l
            for c in content:
                cc = dict(id=c.id, pic=c.pic.d_min)
                pics.append(cc)
            for i in range(s):
                cc = dict(id=0, pic=get_download_url('image', 'no_pic.jpg'))
                pics.append(cc)

        elif self.category == PageModule.Category.THE_THREE or self.category==PageModule.Category.THREE_CIRCLE:
            content = base.limit(3).all()
            l = len(content)
            s = 3 - l
            for c in content:
                cc = dict(id=c.id, pic=c.pic.d_min)
                pics.append(cc)
            for i in range(s):
                cc = dict(id=0, pic=get_download_url('image', 'no_pic.jpg'))
                pics.append(cc)
        return pics
    
class PageContent(BaseModel):
    __tablename__ = 'page_content'
    __table_args__ = {}
    
    class Status(DisplayEnum):
        AVAILABLE = 1
        DISABLE = 0

        __display_cn__ = {
            AVAILABLE: u'有效',
            DISABLE: u'无效'
        }
        
    class Category(DisplayEnum):
        GROUP = 0
        CHANNEL = 1
        
        __display_cn__ = {
            GROUP: u'专辑',
            CHANNEL: u'频道'
        }    
    

    id = Column(u'id', INTEGER(), nullable=False,primary_key=True,autoincrement=True)
    module_id = Column(u'module_id', INTEGER(), nullable=False)
    category = Column(u'category', INTEGER(), nullable=False)
    pic_id = Column(u'pic_id', INTEGER(), nullable=False)
    group_id = Column(u'group_id', INTEGER(), nullable=False)
    status = Column(u'status', INTEGER(), nullable=False,default=0)
    createtime = Column(u'createtime', DATETIME(), nullable=False,default=datetime.now())
    modifytime = Column(u'modifytime', DATETIME(), nullable=False,default=datetime.now())
    createby = Column(u'createby', VARCHAR(length=50), nullable=True)
    modifyby = Column(u'modifyby', VARCHAR(length=50), nullable=True)

    @property
    def pic(self):
        return Pic.get(self.pic_id)
    
    @property
    def group(self):
        return Group.get(self.group_id)
