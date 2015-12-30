import math
from django.core.exceptions import *
from  django.db import IntegrityError
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission, ContentType
from Ycms.functions import post, get
from cmsadmin.forms import PermissionForm
from django.template.context_processors import csrf
from django.contrib.auth.decorators import permission_required, login_required

@login_required
def main(request, action='list', _id=0):
    """
    路由
    根据操作名称路由到相应的处理函数
    """

    #操作白名单
    act_list =['list', 'add', 'edit', 'firbid', 'active', 'del', 'ajax']
    try:
        #操作不在白名单则拒绝
        if not action or action not in act_list:
            raise PermissionDenied

        pms_act = PermissionAct()
        #正常处理逻辑
        if action == 'list':
            return pms_act.list(request)
        if action == 'add':
            return pms_act.add(request)
        if action == 'ajax':
            return ajax(request)

    except PermissionDenied:    
        #重定向到首页
        return redirect('admin:index')

    return render_to_response(tpl, ctx)

class PermissionAct(object):
    """
    """

    def list(self, request):
        # 分页操作
        pn = get(request, 'pn')
        p_size = 20
        p_total = math.ceil(Permission.objects.count()/p_size)
        if not pn or pn == '0':
            pn = 1
        pn = abs(int(pn))
        p_next = pn + 1
        if pn > p_total: 
            pn = p_total
        if p_next > p_total:
            p_next = p_total
        start = p_size*(pn - 1) + 1
        end = start + p_size
        if pn - 1:
            p_prev = pn - 1
        else:
            p_prev = 1
        p_list = list(range(p_total + 1))[1:]
        print(p_list)

        rs = Permission.objects.all()[start:end]

        ctx = {'pn':pn, 'p_list':p_list, 'p_next':p_next,
               'p_prev':p_prev,'p_total':p_total, 'rs':rs}
        return render_to_response('admin/permission.html', ctx)

    def add(self, request):
        """
        需要添加到对应的 content_type上面
        """
        # 检查是否提交内容 
        if not post(request, 'do_submit'):
            # 获取django_content_type
            # TODO: 根据app->model(表）生成二级级联菜单
            rs_content_type = ContentType.objects.raw(' select id, app_label as appname, model as modelname from django_content_type')
            print(rs_content_type[1].model)
            tpl = 'admin/permission_add.html'
            ctx = {'content_type': rs_content_type}
            return render_to_response(tpl, ctx)
        else:
            # 入库
            # 检查contenttype是否存在
            codename = post(request, 'codename')
            name = post(request, 'name')
            content_type_id = post(request, 'content_type_id')
            if not (codename and name and content_type_id):
                tpl, ctx = 'admin/msg.html', {'title':'错误',
                                              'content':'数据提交不完整'}
            else:     
                if ContentType.objects.get(id=content_type_id):
                    o_permission = Permission.objects.create(content_type_id=content_type_id,
                                                             codename=codename, 
                                                             name=name) 
                    o_permission.save()
                    tpl, ctx = 'admin/msg.html', {'title':'提示',
                                              'content':'添加权限成功!'}

                else:
                    # 出错
                    tpl, ctx = 'admin/msg.html', {'title':'错误',
                                              'content':'暂时无法新建权限!'}
            return render_to_response(tpl, ctx) 
