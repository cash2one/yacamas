import os, math, re
import datetime as dt
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required, permission_required
from Ycms.functions import post, get, get_tpl_list
from Ycms.tree import CategoryTree as CateTree
from appcms.models import Category, Archive, Position
from cmsadmin.forms import ArchiveForm
from cmsadmin.models import UserGet
from django.contrib.auth.decorators import permission_required, login_required

@login_required
def main(request, action='list'):
    # 白名单
    act_list = ['add', 
                'edit', 
                'preview', 
                'list',
                'del']
    if not action in act_list:
        redirect('admin:archive_list')
    # 路由
    if action == 'add':
        return archive_act.add_act(request)
    if action == 'edit':
        return archive_act.edit_act(request)
    if action == 'preview':
        return archive_act.preview_act(request)
    if action == 'list':
        return archive_act.list_act(request)
    if action == 'del':
        return archive_act.del_act(request)
    else:
        # 否则重定向
        redirect('admin:archive_list')


# 业务逻辑类
@login_required
class archive_act(object):
    """
    """
    def add_act(request):
        """
        添加
        """
        # 检查是否显示表单

        if not post(request, 'do_submit'):
            # 获取分类列表
            cate_list = Category.get_tree_as_options()
            # 获取广告位列表
            position_list = Position.get_all_as_checkbox()
            # 显示表单
            user_list = UserGet.all_as_option()
            # tpl list of content
            _tpl_list = get_tpl_list('cms')
            tpl_list = []
            if _tpl_list:
                for tpl in _tpl_list:
                    if re.search('^page', tpl):
                        tpl_list.append(tpl)
            tpl, ctx = 'admin/archive_add.html', {'cates': cate_list,
                                              'user_list': user_list,
                                              'tpl_list': tpl_list,
                                              'pos_list': position_list}
        else:
            # 手工获取post数据
            pos_ids = request.POST.getlist('position_id')
            pos_id = []
            if pos_ids:
                for p_id in pos_ids:
                    pos_id.append(p_id + ',')
            pos_id = ''.join(pos_id)
            pos_id = pos_id[:len(pos_id) - 1]
            now = dt.datetime.now()

            data = {'title': post(request, 'title'),
                    'summary': post(request, 'summary'),
                    'content': post(request, 'content'),
                    'keywords': post(request, 'keywords'),
                    'description': post(request, 'description'),
                    'cate_id': post(request, 'cate_id'),
                    'author': post(request, 'author'),
                    'referer': post(request, 'referer'),
                    'create_time': now,
                    'last_edit_time': now,
                    'position_id': pos_id
                    }
            form = ArchiveForm(data)


            if form.is_valid():
                # 入库
                try:
                    o_archive = Archive.objects.create(
                                    title = form.cleaned_data['title'], 
                                    summary = form.cleaned_data['summary'],
                                    content = form.cleaned_data['content'],
                                    keywords = form.cleaned_data['keywords'],
                                    description = form.cleaned_data['description'],
                                    cate_id = form.cleaned_data['cate_id'],
                                    author = form.cleaned_data['author'],
                                    referer = form.cleaned_data['referer'],
                                    create_time = form.cleaned_data['create_time'],
                                    last_edit_time = now,
                                    position_id = form.cleaned_data['position_id'] ,
                                    tpl=post(request, 'tpl')
                                )
                    o_archive.save()
                    tpl, ctx = 'admin/msg.html', {'title':'提示',
                                                  'content':'添加新文章成功！'}
                except:
                    tpl, ctx = 'admin/msg.html', {'title':'错误',
                                                 'content':'.无法添加新文章！'}
            else:
                print(form.errors)
                tpl, ctx = 'admin/msg.html', {'title':'错误',
                                              'content':'无法添加新文章！',
                                              'err_msg': form.errors}
        return render_to_response(tpl, ctx)

        # 处理输入并入库
        


    def edit_act(request):
        """
        添加
        """
        # 检查是否显示表单
        if not post(request, 'do_submit'):
            # 获取分类列表
            cate_list = Category.get_tree_as_options()
            # 获取广告位列表
            position_list = Position.get_all_as_checkbox()
            # 取得本文章内容
            a_id = get(request, 'aid')
            o_arch = Archive.objects.filter(id=a_id).values()[0]
            #print(type(o_arch['author']))
            # 获取cate_name

            if not o_arch:
                tpl, ctx = 'admin/msg.html', {'title':'错误',
                                              'content':'该文章不存在！'}
            else:
                # tpl list of content
                _tpl_list = get_tpl_list('cms')
                tpl_list = []
                if _tpl_list:
                    for tpl in _tpl_list:
                        if re.search('^page', tpl):
                            tpl_list.append(tpl)
                #print(_tpl_list)

                # 显示表单
                user_list = UserGet.all_as_option()
                tpl, ctx = 'admin/archive_edit.html', {'cates': cate_list,
                                                  'user_list': user_list,
                                                  'tpl_list': tpl_list,
                                                  'pos_list': position_list,
                                                  'archive': o_arch}
        else:
            # 手工获取post数据
            pos_ids = request.POST.getlist('position_id')
            pos_id = []
            if pos_ids:
                for p_id in pos_ids:
                    pos_id.append(p_id + ',')
            pos_id = ''.join(pos_id)
            pos_id = pos_id[:len(pos_id) - 1]
            now = dt.datetime.now()
            data = {'title': post(request, 'title'),
                    'summary': post(request, 'summary'),
                    'content': post(request, 'content'),
                    'keywords': post(request, 'keywords'),
                    'description': post(request, 'description'),
                    'cate_id': post(request, 'cate_id'),
                    'author': post(request, 'author'),
                    'referer': post(request, 'referer'),
                    'create_time': now,
                    'last_edit_time': now,
                    'position_id': pos_id
                    }
            form = ArchiveForm(data)


            if form.is_valid():
                # 入库
                try:
                    o_archive = Archive.objects
                    o_archive.filter(id=post(request, 'aid')).update(
                                    title = form.cleaned_data['title'], 
                                    summary = form.cleaned_data['summary'],
                                    content = form.cleaned_data['content'],
                                    keywords = form.cleaned_data['keywords'],
                                    description = form.cleaned_data['description'],
                                    cate_id = form.cleaned_data['cate_id'],
                                    author = form.cleaned_data['author'],
                                    referer = form.cleaned_data['referer'],
                                    create_time = form.cleaned_data['create_time'],
                                    last_edit_time = now,
                                    tpl = post(request, 'tpl'),
                                    position_id = form.cleaned_data['position_id'] 
                                )
                    tpl, ctx = 'admin/msg.html', {'title':'提示',
                                                  'content':'修改文章成功！'}
                except:
                    tpl, ctx = 'admin/msg.html', {'title':'错误',
                                                  'content':'无法修改文章！'}
                    raise
            else:
                tpl, ctx = 'admin/msg.html', {'title':'错误',
                                              'content':'无法修改文章！',
                                              'err_msg': form.errors}
        return render_to_response(tpl, ctx)



    def preview_act(request):
        pass

    def list_act(request):
        """
        列表
        """
        # 分页获取内容
        # 显示
        pn =  abs(int(get(request, 'pn'))) or 1
        # 分页参数
        p_size = 20 
        item_total = Archive.objects.count()
        p_total = math.ceil(item_total/p_size) 
        pn = min(p_total, pn)
        p_next = min(p_total, pn + 1)
        p_prev = max(1, pn - 1)
        # 当页内容
        start = p_size * (pn - 1)
        end   = p_size + start
        rs = Archive.objects.all()[start:end]
        cate_list = list(Category.get_all_as_dict())
        if not rs:
            tpl, ctx = 'admin/msg.html', {'title':'错误',
                                          'content':'系统内还没有文章！'}
        else:
            p_list = [p for p in range(1, p_total + 1)]
            ctx = {'pn': pn, 'p_next':p_next, 'p_prev':p_prev, 'p_total':p_total,
                   'p_list':p_list,'rs': rs, 'cate_list': cate_list}
        return render_to_response('admin/archive.html', ctx)
 
    def del_act(request):
        pass

