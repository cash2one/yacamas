import math
from django.core.exceptions import *
from  django.db import IntegrityError
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import Group, Permission
from Ycms.functions import post, get
from cmsadmin.forms import GroupForm
from cmsadmin.models import AuthActions
from django.contrib.auth.decorators import permission_required, login_required

@login_required
def main(request, action='list', _id=0):
    """
    路由
    根据操作名称路由到相应的处理函数
    """

    #操作白名单
    act_list =['list', 'add', 'addprem', 'edit', 'firbid', 'active', 'del', 'ajax']
    try:
        #操作不在白名单则拒绝
        if not action or action not in act_list:
            raise PermissionDenied

        group_act = GroupAct()
        #正常处理逻辑
        if action == 'list':
            tpl, ctx = group_act.group_list(request)
        if action == 'add':
            tpl, ctx = group_act.group_add(request)
        if action == 'edit':
            tpl, ctx = group_act.group_edit(request)
        if action == 'firbid':
            tpl, ctx = group_act.group_firbid(request)
        if action == 'active':
            tpl, ctx = group_act.group_active(request)
        if action == 'addperm':
            tpl, ctx = group_act.group_addperm(request)
        if action == 'del':
            tpl, ctx = group_act.group_del(request)
        if action == 'ajax':
            return ajax(request)

    except PermissionDenied:    
        #重定向到首页
        return redirect('admin:index')

    return render_to_response(tpl, ctx)

class GroupAct(object):
    """
    group 操作方法
    """ 
    def group_list(self, request):
        """
        group 列表展示
        参数：
            pn 当前page number
        """
        pn =  abs(int(post(request, 'pn'))) or 1

        #rs = Group.objects.raw('drop table cmsadmin_archive')
        #print(rs)
        ppn = 'pn' in request.POST and request.POST['pn']
        # 分页参数
        p_size = 20
        item_total = Group.objects.count()
        p_total = math.ceil(item_total/p_size) 
        pn = min(p_total, pn)
        p_next = min(p_total, pn + 1)
        p_prev = max(1, pn - 1)
        # 当页内容
        start = p_size * (pn - 1)
        end   = p_size + start
        rs = Group.objects.all()[start:end]
        p_list = [p for p in range(1, p_total + 1)]
        ctx = {'pn': pn, 'ppn':ppn, 'p_next':p_next, 'p_prev':p_prev, 'p_total':p_total,
               'p_list':p_list,'rs': rs}
        return ('admin/group.html', ctx)
        
    def group_add(self, request):
        """
        """
        # 显示表单
        if request.method != 'POST':
            g_form = GroupForm()
            perm_dict= AuthActions.get_perm_list_tree()
            #print(perm_dict)
            rtn = 'admin/group_add.html', {'perm_dict': perm_dict, 'form': g_form} 
            return rtn


        name = post(request, 'name')
        # TODO: forms.py 中验证name合法性
        if not name:
            rtn = 'admin/msg.html', {'title':'错误', 'content':'组名不能为空'}
        else:
            # 入库
            try:
                o_group = Group.objects.create(name=name)
                o_group.save()
                o_group.permissions = request.POST.getlist('perm')
                o_group.permissions.add()
                rtn = 'admin/msg.html', {'title':'提示', 'content':'添加权限组成功'}
            
            except IntegrityError:
                rtn = 'admin/msg.html', {'title':'错误',
                                         'content':'权限组名称已经存在!'}

        return rtn

    def group_edit(self, request):
        """
        编辑权限
        """
        gid = max(int(get(request, 'gid')), 0)
        if not gid :
            rtn = 'admin/msg.html', {'title':'错误', 'content':'该权限组不存在！'}
            return rtn
        # 显示表单
        if not post(request, 'do_submit'):
            try:
                rs = Group.objects.get(id=gid)
                g_data = {'name': rs.name}
                print(rs.permissions.all())
                g_form = GroupForm(g_data)
                perm_dict= AuthActions.get_perm_list_tree()
                back_url = request.META['HTTP_REFERER']
                rtn = 'admin/group_edit.html', {'perm_dict':perm_dict, 
                                                'group_perms': [perm.id for perm in rs.permissions.all()],  
                                                'form': g_form, 'gid':gid}
            except :
                raise
        else:
            # 入库
            name = post(request, 'name')
            g_form = GroupForm({'name': name, 'id':gid})
            # 无论是否修改名称都要重新授权
            o_group = Group.objects.get(id=gid)
            o_group.permissions.clear()
            # o_group.permissions = [] 
            # o_group.permissions.add() 这两句同上面的clear() 等效
            o_group.permissions = request.POST.getlist('perm')
            o_group.permissions.add()

            # 先清空权限
            # 再update 组
            # 再添加权限
            g_form.is_valid()
            v_data = g_form.cleaned_data
            if v_data and 'name' in v_data:
                Group.objects.filter(id=gid).update(name=name)
                rtn = 'admin/msg.html', {'title':'提示', 'content':'修改权限组成功'}
            else:
                rtn = 'admin/msg.html', {'title':'提示', 'content':'用户授权成功!'}
        return rtn
            
    def group_del(self, request):
        
        # TODO: 删除前需要 js 弹出确认对话框
        # 要删除引用group的其他表中的条目
        gid = max(int(get(request, 'gid')), 0)
        print(gid)
        try:
            o_group = Group.objects.filter(id=gid)
            o_group.delete()
            # 下一步删除auth_group_permissions auth_user_groups 中对应的groupid
            del_premission_group = Group.objects.raw('delete from `auth_group_premissions` where `group_id` = gid')
            del_auth_user_groups = Group.objects.raw('delete from `auth_user_groups` where `group_id` = gid')
            rtn = 'admin/msg.html', {'title': '提示', 'content':'权限组删除成功'}
        except:
            
            rtn = 'admin/msg.html', {'title': '错误', 'content':'权限组删除出错!'}
            raise
        return rtn

    

########## 私有方法 ##########

    def _group_permission(self, request):
        """
        group 授权
        添加permissions到group
        """
        # 取得gid
        gid = int(post(request, 'gid'))
        # 取得permissions  类似 1，2，3，4，5 逗号隔开的数字字符串
        pms = post(request, 'pms')
        if not gid or not pms:
            return False
        # 添加 gid：group_id pms：premission_id 到表： auth_group_permissions
        # 加工 permissions 字符串
        # insert into `auth_group_permissions` (`group_id`, `permission_id`)
        #   values (gid, pms_id)
        list_pms = pms.split(',')
        query_str = ['insert into `auth_group_permissions` (`group_id`, `permission_id`) ']
        for pms_id in list_pms:
            if int(pms_id):
                query_str.append(' values(' + str(gid) + ', ' + str(pms_id) + ') ')
                
        return  Group.objects.raw(query_str.join)
        
        
