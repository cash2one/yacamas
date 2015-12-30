import math, re
from django.core.exceptions import *
from  django.db import IntegrityError
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect

from appcms.models import Position
from Ycms.functions import post, get
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

        positionAct = PositionAct()
        #正常处理逻辑
        if action == 'list':
            return positionAct.list_act(request)
        if action == 'add':
            return positionAct.add_act(request)
        if action == 'edit':
            return positionAct.edit_act(request)
        if action == 'firbid':
            return positionAct.firbid_act(request)
        if action == 'active':
            return positionAct.active_act(request)
        if action == 'del':
            return positionAct.del_act(request)
        if action == 'ajax':
            return ajax(request)

    except PermissionDenied:    
        #重定向到首页
        return redirect('admin:index')

    return render_to_response(tpl, ctx)

class PositionAct(object):

    def add_act(self, request):
        """
        添加
        """
        if not post(request, 'do_submit'):
            # 显示表单
            tpl, ctx = 'admin/position_add.html', {}
        else:
            name = post(request, 'name')
            if re.match(re.compile(r'^[\u4e00-\u9fa5\w-]{2,30}$'), name):
                # 入库
                o_pos = Position.objects.create(name=name)
                try:
                    o_pos.save()
                    tpl, ctx = 'admin/msg.html', {'title':'提示','content':'添加成功!'}
                except:
                    tpl, ctx = 'admin/msg.html', {'title':'错误','content':'无法添加推荐位!'}

            else:
                tpl, ctx = 'admin/msg.html', {'title':'错误','content':'无法添加推荐位{0}'.format(name)}
        return render_to_response(tpl, ctx)
    
