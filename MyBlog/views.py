#coding:utf-8
from pyramid.view import view_config
from datetime import datetime
from models import *
from forms import *
from pyramid.security import remember, forget,authenticated_userid
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

@view_config(route_name='index',
             renderer='templates/index.mako')
def index (request):
    entry=Article.get_all(request)#发表时间排序
    #entry=request.dbsession.query(Article).order_by(Article.date).all()
    userid=authenticated_userid(request)  #返回已认证的用户,如果为空则未登录
    if not entry:
        return HTTPNotFound
    return {'rows':entry,'userid':userid}

@view_config(route_name='admin',
             renderer='templates/login.mako')
def login (request):
    form=LoginForm(request.POST)
    if request.method=='POST' and form.validate():
        admin=request.dbsession.query(Admin).filter_by(
            name=form.username.data.encode('utf-8')).first()#不转换会报UnicodeEncodeError: 'latin-1' codec can't encode character
        if admin :
            headers=remember(request,admin.name)
        else:
            headers=forget(request)
        return  HTTPFound(location=request.route_url('index'),headers=headers)
    if request.method=='GET' and request.params.get("do",0)=='out':
        headers = forget(request)
        return HTTPFound(location=request.route_url('index'), headers=headers)
    return {'form': form}

@view_config(route_name='blog_action',
             match_param='action=create',
             renderer='templates/edit.mako',
             permission='edit')
def blog_create(request):#添加
    entry = Article()
    form=BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        request.dbsession.add(entry)
        entry.update_cache(request)#更新缓存
        return HTTPFound(location=request.route_url('index'))
    return {'form': form, 'action': request.matchdict.get('action')}

@view_config(route_name='blog_action',
             match_param='action=update',
             renderer='templates/edit.mako',
             permission='edit')
def blog_update(request):#修改
    blog_id = int(request.params.get('uid', -1))#这里一定要用request.params.get,不要用request.GET.get不然post时找不到entry
    entry = request.dbsession.query(Article).get(blog_id)
    if not entry:
        return HTTPFound(location=request.route_url('index'))
    form=BlogUpdateForm(request.POST,entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.update_cache(request)#更新缓存
        return HTTPFound(location=request.route_url('index'))
    return {'form': form, 'action': request.matchdict.get('action')}

@view_config(route_name='blog_action',
             match_param='action=delete',
             permission='edit')
def blog_delete(request):
    blog_id = int(request.GET.get('uid', -1))
    entry = request.dbsession.query(Article).get(blog_id)
    if  entry:
        request.dbsession.delete(entry)
        entry.update_cache(request)#更新缓存
    return HTTPFound(location=request.route_url('index'))

@view_config(route_name='blog_view',renderer='templates/view.mako')
def blog_view(request):#查看
    #request.GET.get('id', -1)
    blog_id = int(request.GET.get('uid', -1))
    entrys=Article.get_all(request)
    entry =filter(lambda x:x.uid==blog_id,entrys).pop()
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}
