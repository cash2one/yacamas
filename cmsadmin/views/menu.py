from django.shortcuts import render_to_response, redirect
from appcms.models import Menu 
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
                'del']
    if not action in act_list:
        redirect('admin:menu_act', action='list')
    # 路由
    if action == 'add':
        return MenuAdmin.add_act(request)
    if action == 'edit':
        return MenuAdmin.edit_act(request)
    if action == 'preview':
        return MenuAdmin.preview_act(request)
    if action == 'list':
        return MenuAdmin.list_act(request)
    if action == 'del':
        return MenuAdmin.del_act(request)
    else:
        # 否则重定向
        redirect('admin:category_list')


# 业务逻辑类

class MenuAdmin(object):
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
        
        if not request.method == 'POST':
            # 获取分类列表
            # 显示表单
            menu_list = Menu.objects.all().values()
            #print(menu_list)
            o_tree = CateTree(menu_list)
            menus = o_tree.tree(seprator=' .&nbsp; ', 
                                wrapper='<option value="{2}">{0}</option>', 
                                wrapper_all=True)
            
            #print(menus)
            tpl, ctx = 'admin/menu_add.html', {'menu_tree_select': menus}

            return render_to_response(tpl, ctx)

        # 处理输入并入库
        # TODO: menu 模型没有定义form类进行数据验证
        else:
            # pid / path / has_child / depth
            pid = int(post(request, 'pid'))
            name=post(request, 'name')
            m_type = post(request, 'm_type') or 'back'
            url = post(request, 'url')
            code = post(request, 'code')
            list_order = post(request, 'list_order')
            # 检测pid是否为-1 若是则返回错误提示选择父目录
            if pid < 0:
                tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                              'content':'选择一个上级类别或作为”顶级类别“！'}
            elif pid > 0:
                # 获取父cate
                print(pid)
                p_menu = Menu.objects.filter(id=pid).get()
                
                if not p_menu:
                    # 父cate不存在
                    tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'父菜单不存在！'}
                else:
                    # 父目录存在 则检测兄弟由无重名 若有则提示出错
                    same_name_siblings = Menu.objects.filter(name=name,
                                                             pid=pid).count()
                    if same_name_siblings:
                        tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'相同父类别下已经有该名称分类！'}
                        return render_to_response(tpl, ctx)
                    else:
                        # 没有同名兄弟 可以提交（pid/name在上面已经赋值）
                        path = p_menu.path + ',' + str(pid)
                        depth = int(p_menu.depth) + 1
                        p_has_child = p_menu.has_child
            elif pid <= 0:
                path = 0
                depth = 0
            # 本cate入库
            menu = Menu.objects.create(path=path,
                                       name=name,
                                       m_type=m_type,
                                       code=code,
                                       url=url,
                                       depth=depth,
                                       list_order = list_order,
                                       pid=pid,
                                       has_child=0
                                       )
            try:
                menu.save()
                # 若父cate的has_child 为0 则修改为1 否则不操作
                if pid and not p_has_child:
                    Menu.objects.filter(id=pid).update(has_child=1)
                #return redirect('admin:category_act', action='list')
                tpl, ctx = 'admin/msg.html', {'title':'提示', 
                                              'content':'添加分类成功！'}

            except:
                tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                              'content':'添加分类出错！'}

            return render_to_response(tpl, ctx)
        


    def edit_act(request):
        # 检查是否显示表单
        
        if not request.method == 'POST':
            # 获取分类列表
            # 显示表单
            mid = get(request, 'mid')
            menu_list = Menu.objects.all().values()
            o_tree = CateTree(menu_list)
            menus = o_tree.tree(seprator=' .&nbsp; ', 
                                wrapper='<option value="{2}">{0}</option>', 
                                wrapper_all=True)
            
            o_menu = Menu.objects.get(id=mid)
            tpl, ctx = 'admin/menu_edit.html', {'o_menu':o_menu, 'menu_tree_select': menus}

            return render_to_response(tpl, ctx)

        # 处理输入并入库
        # TODO: menu 模型没有定义form类进行数据验证
        else:
            # pid / path / has_child / depth
            pid = int(post(request, 'pid'))
            name=post(request, 'name')
            m_type = post(request, 'm_type') or 'back'
            url = post(request, 'url')
            code = post(request, 'code')
            list_order = post(request, 'list_order')
            # 检测pid是否为-1 若是则返回错误提示选择父目录
            if pid < 0:
                tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                              'content':'选择一个上级类别或作为”顶级类别“！'}
            elif pid > 0:
                # 获取父cate
                p_menu = Menu.objects.filter(id=pid).get()
                
                if not p_menu:
                    # 父cate不存在
                    tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'父菜单不存在！'}
                else:
                    # 父目录存在 则检测兄弟由无重名 若有则提示出错
                    same_name_siblings = Menu.objects.filter(name=name,
                                                             pid=pid).count()
                    if same_name_siblings:
                        tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                                  'content':'相同父类别下已经有该名称分类！'}
                        return render_to_response(tpl, ctx)
                    else:
                        # 没有同名兄弟 可以提交（pid/name在上面已经赋值）
                        path = p_menu.path + ',' + str(pid)
                        depth = int(p_menu.depth) + 1
                        p_has_child = p_menu.has_child
            elif pid <= 0:
                path = 0
                depth = 0
            # 本cate入库
            menu = Menu.objects.filter(id=get(request, 'mid'))
            try:
                menu.update(path=path,
                                       name=name,
                                       m_type=m_type,
                                       code=code,
                                       list_order=list_order,
                                       url=url,
                                       depth=depth,
                                       pid=pid,
                                       has_child=0
                                       )
                # 若父cate的has_child 为0 则修改为1 否则不操作
                if pid and not p_has_child:
                    Menu.objects.filter(id=pid).update(has_child=1)
                #return redirect('admin:category_act', action='list')
                tpl, ctx = 'admin/msg.html', {'title':'提示', 
                                              'content':'添加菜单成功！'}

            except:
                tpl, ctx = 'admin/msg.html', {'title':'错误', 
                                              'content':'添加菜单出错！'}

            return render_to_response(tpl, ctx)
 

    def move_act(request):
        pass

    def preview_act(request):
        pass

    def list_act(request):
        menu_list = Menu.objects.all().values()

        return render_to_response('admin/menu.html',
                                  {'menu_list':menu_list})
        

    def del_act(request):
        pass

