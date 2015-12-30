from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import permission_required, login_required
from Ycms.functions import post, get
#from django.template.context_processors import csrf
@login_required
def idx(request):
    """
    后台首页
    需要检查权限，若未登录或不是管理员要跳转到登录页面
    """
    # do somthing

    return render_to_response('admin/index.html', {'user':request.user})

@login_required
@permission_required('appcms.add_archive')
def summary(request):
    """
    后台首页 在右侧 iframe中显示
    显示内容：管理员欢迎页
    """
   # print(dir(request.user))
   # print(request.user.get_group_permissions())
   # print(request.user.has_perm('appcms.add_archive'))

    return render_to_response('admin/summary.html',{'user':request.user})

def login(request):
    if request.method == 'POST':
        # 根据输入的用户名获取user
        user_name = post(request, 'user_name').replace(' ', '').replace("'", '')
        pwd = post(request, 'pwd')
        # 将user传入 login
        ouser = auth.authenticate(username=user_name, password=pwd)
        if ouser and ouser.is_active:
            auth.login(request, ouser)
        else:
            return render_to_response('admin/msg.html', {'title':'错误',
                                                         'content':'用户名或密码错误！'})
        return redirect('/manage/')
    else:
        # 登录表单
        return render_to_response('admin/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/manage/')
