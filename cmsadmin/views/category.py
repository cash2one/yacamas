import re, math
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response, redirect
from appcms.models import Category as Cate
from cmsadmin.forms import CateForm
from Ycms.functions import post, get
from Ycms.tree import CategoryTree as CateTree
from django.contrib.auth.decorators import permission_required, login_required

@login_required
def main(request, action='list'):
    # 白名单
    act_list = ['add', 
                'edit', 
                'preview', 
                'list',
                'forbid',
                'del']
    if not action in act_list:
        redirect('admin:category_act')
    # 路由
    if action == 'add':
        return CateAdmin.add_act(request)
    if action == 'edit':
        return CateAdmin.edit_act(request)
    if action == 'preview':
        return CateAdmin.preview_act(request)
    if action == 'list':
        return CateAdmin.list_act(request)
    if action == 'del':
        return CateAdmin.del_act(request)
    if action == 'forbid':
        return CateAdmin.forbid_act(request)
    else:
        # 否则重定向
        redirect('admin:category_list')


# 业务逻辑类

class CateAdmin(object):
    """
    TODO: cate: form 约束/验证字段
    TODO: cate: 更多字段： 描述/seo等等
    TODO: cate: move/edit/del等
    """
    def add_act(request):
        """
        添加
        """
        # 检查是否显示表单
        
        if request.method != 'POST':
            # 获取分类列表
            # 显示表单
            cate_list = Cate.objects.all().values()
            o_form = CateForm()
            o_tree = CateTree(cate_list)
            cates = o_tree.tree(seprator=' .&nbsp; ', 
                                wrapper='<option value="{2}">{0}</option>', 
                                wrapper_all=True)
            
            tpl, ctx = 'admin/cate_add.html', {'form':o_form, 'cate_tree_select': cates}

            return render_to_response(tpl, ctx)

        # 处理输入并入库
        # TODO: category 模型没有定义form类进行数据验证
        else:
            # pid / path / has_child / depth
            pid = int(post(request, 'pid'))
            name=post(request, 'name')
            alias = post(request, 'alias')
            cate_type = post(request, 'cate_type')
            #print(cate_type)
            # 检测pid是否为-1 若是则返回错误提示选择父目录
            if pid < 0:
                tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                              'content':'选择一个上级分类或作为”顶级分类“！'}
                return render_to_response(tpl, ctx)
            elif pid > 0:
                # 获取父cate
                print(pid)
                p_cate = Cate.objects.filter(id=pid).get()
                
                if not p_cate:
                    # 父cate不存在
                    tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'父分类不存在！'}
                else:
                    # 父目录存在 则检测兄弟由无重名 若有则提示出错
                    same_name_siblings = Cate.objects.filter(name=name,
                                                             pid=pid).count()
                    if same_name_siblings:
                        tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'相同父分类下已经有该名称分类！'}
                        return render_to_response(tpl, ctx)
                    else:
                        # 没有同名兄弟 可以提交（pid/name在上面已经赋值）
                        path = p_cate.path + ',' + str(pid)
                        depth = int(p_cate.depth) + 1
                        p_has_child = p_cate.has_child
            elif pid == 0:
                path = 0
                depth = 0
            # 本cate入库
            alias = alias.strip(' ')
            o_form = CateForm({'name':name, 'cate_type':cate_type, 'alias':alias, 'path':path})
            if (o_form.is_valid()):
                alias, cnt = re.subn(r' +', '-', alias)
                #print(alias)
                cate = Cate.objects.create(path=path,
                                       name=name,
                                       depth=depth,
                                       pid=pid,
                                       alias=alias,
                                       has_child=0
                                       )
                try:
                    cate.save()
                    # 若父cate的has_child 为0 则修改为1 否则不操作
                    if pid and not p_has_child:
                        Cate.objects.filter(id=pid).update(has_child=1)
                    #return redirect('admin:category_act', action='list')
                    tpl, ctx = 'admin/msg.html', {'title':'提示', 
                                                  'content':'.添加分类成功！'}

                except:
                    tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'..添加分类出错！'}
            else:
               # FIXIT: 无端提示 cate_type 为必填项 
               print(o_form.errors)
               tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'添加分类出错！'}


        return render_to_response(tpl, ctx)
        


    def edit_act(request):
        cid = get(request, 'cid')
        if request.method == 'GET':
            if not cid:
                tpl, ctx = 'admin/msg.html', {'title':'提示', 
                                              'content':'.分类不存在！'}
            else:
                try:
                    oCate = Cate.objects.get(id=cid)
                    cate_list = Cate.objects.all().values()
                    o_form = CateForm()
                    o_tree = CateTree(cate_list)
                    cates = o_tree.tree(seprator=' .&nbsp; ', 
                                        wrapper='<option value="{2}">{0}</option>', 
                                        wrapper_all=True)

                    tpl, ctx = 'admin/cate_edit.html', {'form':o_form, 'oCate': oCate,
                                                        'cate_tree_select':cates}
                    print(oCate)
                except:
                    tpl, ctx = 'admin/msg.html', {'title':'提示', 
                                                  'content':'分类不存在！'}

            return render_to_response(tpl, ctx)
        else:
            pid = int(post(request, 'pid'))
            cid = int(post(request, 'cid'))
            name=post(request, 'name')
            alias = post(request, 'alias')
            cate_type = post(request, 'cate_type')
            #print(cate_type)
            # 检测pid是否为-1 若是则返回错误提示选择父目录
            #print(cate_type)
            if pid < 0:
                tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                              'content':'选择一个上级分类或作为”顶级分类“！'}
                return render_to_response(tpl, ctx)
            elif pid > 0:
                # 获取父cate
                p_cate = Cate.objects.filter(id=pid).get()
                
                if not p_cate:
                    # 父cate不存在
                    tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'父分类不存在！'}
                else:
                    # 父目录存在 则检测兄弟由无重名 若有则提示出错
                    same_name_siblings = Cate.objects.filter(name=name,
                                                             pid=pid)
                    siblings_cnt = same_name_siblings.count()
                    if siblings_cnt > 1:
                        tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'相同父分类下已经有该名称分类！'}
                        return render_to_response(tpl, ctx)
                    else:
                        # 没有同名兄弟 可以提交（pid/name在上面已经赋值）
                        path = p_cate.path + ',' + str(pid)
                        depth = int(p_cate.depth) + 1
                        p_has_child = p_cate.has_child
            elif pid == 0:
                path = 0
                depth = 0
            # 本cate入库
            alias = alias.strip(' ')
            o_form = CateForm({'name':name, 'cate_type':cate_type,'alias':alias,  'path':path})
            if (o_form.is_valid()):
                alias, cnt = re.subn(r' +', '-', alias)
                #print(alias)
                try:
                    Cate.objects.filter(id=cid).update(path=path,
                                       name=name,
                                       cate_type=cate_type,
                                       depth=depth,
                                       pid=pid,
                                       alias=alias,
                                       has_child=0)
                    # 若父cate的has_child 为0 则修改为1 否则不操作
                    if pid and not p_has_child:
                        Cate.objects.filter(id=pid).update(has_child=1)
                    #return redirect('admin:category_act', action='list')
                    tpl, ctx = 'admin/msg.html', {'title':'提示', 
                                                  'content':'编辑分类成功！'}

                except:
                    tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'..编辑分类出错！'}
                    raise
            else:
               # FIXIT: 无端提示 cate_type 为必填项 
               tpl, ctx = 'admin/msg.html', {'title':'错误',
                                                  'content':'编辑分类出错！'}


        return render_to_response(tpl, ctx)


    def forbid_act(request):
        cid = int(get(request, 'cid'))
        act = get(request, 'act')
        dictAct = {'active':99, 'forbid':1, 'del':'0'}
        try:
            Cate.objects.filter(id=cid).update(status=dictAct[act.replace(' ',
                                                                          '')])
        except:
            tpl, ctx = 'admin/msg.html', {'title':'错误',
                                              'content':'操作失败！'}
            return render_to_response(tpl, ctx)
        return redirect('admin:category_act', action='list')



    def preview_act(request):
        pass

    def list_act(request):
        """
        列表
        """
        # 分页获取内容
        # 显示
        cn =  abs(int(get(request, 'cn'))) or 1
        # 分页参数
        c_size = 20 
        item_total = Cate.objects.count()
        c_total = math.ceil(item_total/c_size) 
        cn = min(c_total, cn)
        c_next = min(c_total, cn + 1)
        c_prev = max(1, cn - 1)
        # 当页内容
        start = c_size * (cn - 1)
        end   = c_size + start
        rs = Cate.objects.order_by('id')[start:end]
        if not rs:
            tpl, ctx = 'admin/msg.html', {'title':'错误',
                                          'content':'系统内还没有分类！'}
        else:
            c_list = [c for c in range(1, c_total + 1)]
            ctx = {'cn': cn, 'c_next':c_next, 'c_prev':c_prev, 'c_total':c_total,
                   'c_list':c_list,'rs': rs }
        return render_to_response('admin/category.html', ctx)
 

    def del_act(request):
        pass

