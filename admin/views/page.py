# -*- coding:utf-8 -*-

from flask import render_template, g, request, flash, redirect, url_for
from flask.blueprints import Blueprint
from flask.json import jsonify
#from bg_biz.service.page_view_service import PageViewService
from bg_biz.orm.page import PageModule, PageContent
from sharper.flaskapp.kvdb import kvdb
from sharper.util.transfer import orm_obj2dict

from form import obj2form, form2obj
from form.page import PageModuleForm, PageContentForm

from bg_biz.orm.pic import Group


__author__ = 'John Chan'

PageView = Blueprint('page', __name__)

@PageView.route('/module', methods=['GET','POST'])
def module_list():
    data = request.form or request.args
    g.current_page = data.get("page",PageModule.Page.INDEX)
    basequery = PageModule.query.filter_by(page=g.current_page)
    g.pages = []
    for page in PageModule.Page.AllEnum():
        g.pages.append((page,PageModule.Page.get_display_cn(page)))
    page_modules = basequery.filter_by(status=PageModule.Status.AVAILABLE).order_by(PageModule.rank.desc()).order_by(PageModule.id).all()
    pm_sort(page_modules)
    # sorted(page_modules, cmp=pm_cmp)
    groups = Group.query.filter_by(status=1).order_by(Group.id.desc()).all()
    return render_template("page/page_module_list.html",page_modules=page_modules,groups=groups)

def pm_cmp(o1,o2):
    return int(o1.rank-o2.rank)

def pm_sort(pms):
    index = len(pms)
    for pm in pms:
        if pm.rank != index:
            pm.rank=index
            pm.update()
        index-=1




@PageView.route('/module/<int:id>',methods=['GET'])
def module_edit(id):
    form = PageModuleForm()
    g.current_page = request.args.get("page",None)
    if g.current_page:
        form.page.data = g.current_page
    form.page.choices = [(page, PageModule.Page.get_display_cn(page)) for page in PageModule.Page.AllEnum()]
    form.category.choices = [(category, PageModule.Category.get_display_cn(category)) for category in PageModule.Category.AllEnum()]

    if id:
        page_module = PageModule.get(id)
        if page_module:
            obj2form(page_module,form)
    return render_template("page/page_module_edit.html",form=form)

@PageView.route('/module/<int:id>',methods=['POST'])
def module_update(id):
    form = PageModuleForm(request.form)
    form.page.choices = [(page, PageModule.Page.get_display_cn(page)) for page in PageModule.Page.AllEnum()]
    form.category.choices = [(category, PageModule.Category.get_display_cn(category)) for category in PageModule.Category.AllEnum()]
    if id:
        page_module = PageModule.get(id)
    else:
        page_module = PageModule()
    form2obj(form, page_module)
    if page_module.id:
        page_module.update()
        flash(u'修改页面组件成功', 'ok')
    else:
        page_module.insert()
        flash(u'添加页面组件成功', 'ok')
    clear_page(page_module.page)
    return redirect(url_for("page.module_list", page=page_module.page))


@PageView.route("/module/up",methods=['POST','GET'])
def module_move_up():
    data = request.form or request.args
    g.current_page = data["page"]
    basequery = PageModule.query.filter_by(page=g.current_page)
    page_modules = basequery.filter_by(status=PageModule.Status.AVAILABLE).order_by(PageModule.rank.desc()).order_by(PageModule.id).all()
    last = None
    for pm in page_modules:
        if not last:
            last = pm
            continue
        if pm.id == int(data["id"]):
            tmp = pm.rank
            pm.rank = last.rank
            last.rank = tmp
            pm.update()
            last.update()
            break
        last = pm
    return redirect(url_for("page.module_list",page=g.current_page))


@PageView.route("/module/down",methods=['POST','GET'])
def module_move_down():
    data = request.form or request.args
    g.current_page = data["page"]
    basequery = PageModule.query.filter_by(page=g.current_page)
    page_modules = basequery.filter_by(status=PageModule.Status.AVAILABLE).order_by(PageModule.rank.desc()).order_by(PageModule.id).all()
    last = None
    for pm in page_modules:
        if last:
            tmp = pm.rank
            pm.rank = last.rank
            last.rank = tmp
            pm.update()
            last.update()
            break
        if pm.id == int(data["id"]):
            last = pm
            continue
    return redirect(url_for("page.module_list",page=g.current_page))


@PageView.route('/module/del/<int:id>',methods=['GET'])
def module_del(id):
    m = PageModule.get(id)
    m.status = PageModule.Status.DISABLE
    m.update()
    return redirect(url_for("page.module_list",page=request.args['page']))


@PageView.route('/content',methods=['GET','POST'])
def content_list():
    data = request.form or request.args
    g.pages = []
    g.modules = []
    g.current_module_id = 0
    for page in PageModule.Page.AllEnum():
        g.pages.append((page,PageModule.Page.get_display_cn(page)))

    if data.has_key('page'):
        g.current_page = data['page']
    else:
        g.current_page = PageModule.Page.INDEX
    for module in PageModule.query.filter_by(page=g.current_page).filter_by(status=PageModule.Status.AVAILABLE).all():
        if module.category == PageModule.Category.SPLIT_LINE:
            continue
        if not g.modules:
            g.current_module_id = module.id
        g.modules.append((module.id,module.desc))
    if data.has_key('module_id'):
        g.current_module_id = data['module_id']
    cs = PageContent.query.filter_by(module_id=g.current_module_id).filter_by(status=PageContent.Status.AVAILABLE).all()
    return render_template("page/content_list.html",cs=cs)

@PageView.route('/content/<int:id>',methods=['GET'])
def get_content(id):
    
    form = PageContentForm()
    g.current_category = Resource.Type.APP
    content = PageContent.get(id)
    choices = []
    current_resource_id = 0
    current_resource = ""
    if content:
        g.current_category = content.category
        g.module_id = content.module_id
        obj2form(content,form)
        current_resource_id = content.resource_id
        current_resource = Resource.get(current_resource_id)
        if current_resource:
            choices.append((current_resource.id,current_resource.desc))
        else:
            choices.append((current_resource_id,u"其他"))
        g.photo = content.image_http
    else:
        g.module_id = request.args['module_id']
        form.module_id.data=g.module_id
    g.module = PageModule.get(g.module_id)
    g.page = g.module.page
    g.page_cn = PageModule.Page.get_display_cn(g.page)
    #对类型为100的其他类型特殊处理
    if g.current_category != 100:
        #如果是app,只查询已经上架的产品
        choices = get_resource_choices(g.current_category,choices,current_resource_id)
    form.resource_id.choices=choices
    form.source_id.data=current_resource.source_id if current_resource else ""
    return render_template("page/content_edit.html", form=form)

@PageView.route('/custom_content',methods=['POST'])
def custom_content():
    data = request.form
    print data
    title = data.get('title',None)
    combobox = data.get('combobox',None)
    id = data.get('id',None)
    module_id = data.get('module_id',None)
    content_id = data.get('content_id',None)
    pic_id = data.get('pic_id', None)
    if module_id and content_id:
        #module=PageModule.get(module_id)
        content = PageContent.get(content_id)
        content.pic_id = pic_id
        content.group_id=combobox
        content.status = 1
        content.update()
    else:
        content = PageContent()
        # content.category = module.category
        content.module_id = module_id
        content.pic_id = pic_id
        content.group_id = combobox
        content.status = 1
        content.insert()
    return redirect(url_for('.module_list'))


@PageView.route('/content/<int:id>',methods=['POST'])
def edit_content(id):
    form = PageContentForm(request.form)
    if id:
        content = PageContent.get(id)
        g.current_category = content.category
    else:
        content = PageContent()
        g.current_category = Resource.Type.APP
    choices = get_resource_choices(g.current_category,[])
#     for res in Resource.query.filter_by(type=g.current_category).order_by(Resource.id.desc()).limit(100).all():
# 
#         choices.append((res.id, res.desc))
    form.resource_id.choices=choices
    if form.validate():
       return render_template("page/content_edit.html", form=form)

    form2obj(form,content)
    if content.category == 100:
        content.action_type = "webview"
    elif content.category == Resource.Type.FORUM_INDEX:
        content.action_type = "activity"
        # content.url = "io.hiwifi.ui.activity.ForumActivity"
        # content.action_uri = "io.hiwifi.ui.activity.ForumActivity"
        content.action_uri = content.url
    if content.id:
        content.update()
        flash(u'修改页面内容成功', 'ok')
    else:
        content.insert()
        flash(u'新建页面内容成功', 'ok')
    g.module_id = content.module_id
    g.module = PageModule.get(g.module_id)
    g.page = g.module.page
    g.page_cn = PageModule.Page.get_display_cn(g.page)
    cache_page(g.page)
    return redirect(url_for("page.get_content",id=content.id))

def cache_page(page):
    ms,mc = PageViewService.get_page_view(page);
    view = render_template("page/page_view.json",ms=ms,mc=mc)
    kvdb.common.hset("page",page,view)
    
def clear_page(page):
    i = kvdb.common.hdel("page",page)

@PageView.route('/resource_type/<int:type>', methods=['GET'])
def resource_type(type):
#     ret = []
#     for res in Resource.query.filter_by(type=type).order_by(Resource.id.desc()).limit(100).all():
#         ret.append((res.id,res.desc))
    return render_template("page/resource_type.html", ret=get_resource_choices(type,[]), resource_id=request.args.get("resource_id", 0))

@PageView.route('/resource/<int:resource_id>/<int:category>', methods=['GET'])
def resource(resource_id,category):
    res = Resource.get_by_type_source(category, resource_id)

    dic = orm_obj2dict(res)
    dic['desc'] = res.desc


    return jsonify(resource=dic)


def get_resource_choices(type,choices=[],current_resource_id=-1):
    if type == Resource.Type.APP:
        for promotion in Promotion.query.filter_by(status=Promotion.Status.AVAILABLE).all():
            res = Resource.query.filter_by(type=type).filter_by(source_id=promotion.apk_id).first();
            if res.id == current_resource_id:
                continue
            choices.append((res.id, res.desc))
    else:
        for res in Resource.query.filter_by(type=type).order_by(Resource.id.desc()).limit(100).all():
            if res.id == current_resource_id:
                continue
            choices.append((res.id, res.desc))
    return choices



