import os, math, re, json
import datetime as dt
from django.shortcuts import render_to_response, redirect
from Ycms.functions import post, get, get_tpl_list
from appcms.models import SysInfo
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
        return SysInfo_act.add_act(request)
    if action == 'edit':
        return SysInfo_act.edit_act(request)
    if action == 'preview':
        # 否则重定向
        redirect('admin:archive_list')


# 业务逻辑类

class SysInfo_act(object):
    """
    """
    def add_act(request):
        """
        添加
        """
        if request.method != 'POST':
            key = get(request, 'key')
            dictTpl = {'siteInfo':'admin/sys-site-info.html',
                       'siteSeo': 'admin/sys-site-seo.html',}
            ctx = {}
            try:
                try:
                    oSysInfo = SysInfo.objects.get(key=key)
                    val = oSysInfo.value
                    ctx = {'keyId':oSysInfo.id, 'oval':json.loads(val)}
                except:
                    pass
                #print(type(json.loads(val)))
                return render_to_response(dictTpl[key], ctx)

            except:
                raise
                raise Http404('内部错误：网页没找到')

        else:
            # print(dir(request.POST))
            # print([i for i in request.post.lists()])
            dictList = request.POST.lists()
            val = {}
            for i in dictList:
                item = val[i[0]] = i[1][0]
            # print(json.dumps(val))
            val = json.dumps(val)

            key = get(request, 'key')
            keyId = post(request, 'keyId')
            value = json.dumps(val)
            try:
                if(keyId):
                    oSysInfo = SysInfo.objects.filter(id=keyId).update(key=key,
                                                                       value=value)
                    tpl, ctx = 'admin/msg.html', {'title':'提示',
                                                  'content':'修改成功！'}
                else:
                    oSysInfo = SysInfo.objects.create(key=key, value=value)
                    oSysInfo.save()
                    tpl, ctx = 'admin/msg.html', {'title':'提示',
                                                  'content':'新建成功！'}
            except:
                tpl, ctx = 'admin/msg.html', {'title':'错误',
                                              'content':'新建失败！'}
                raise 

            return render_to_response(tpl, ctx)
