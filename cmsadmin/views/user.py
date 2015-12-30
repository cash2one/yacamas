import math,os
from django.core.exceptions import *
from  django.db import IntegrityError
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from Ycms.functions import post, get
from django.contrib.auth.decorators import permission_required, login_required

#导入forms
from cmsadmin.forms import *

@login_required
def main(request, action='list'):
    """
    路由
    根据操作名称路由到相应的处理函数
    """

    #操作白名单
    act_list =['list', 'add', 'edit', 'firbid', 'active', 'del', 'ajax', 'info']
    try:
        #操作不在白名单则拒绝
        if not action or action not in act_list:
            raise PermissionDenied

        user_act = UserAct()
        #正常处理逻辑
        if action == 'list':
            tpl, ctx = user_act.user_list(request)
        if action == 'add':
            tpl, ctx = user_act.user_add(request)
        if action == 'edit':
            tpl, ctx = user_act.user_edit(request)
            #print((tpl, ctx))
        if action == 'firbid':
            tpl, ctx = user_act.user_firbid(request)
        if action == 'active':
            tpl, ctx = user_act.user_active(request)
        if action == 'del':
            tpl, ctx = user_act.user_del(request)
        if action == 'info':
            tpl, ctx = user_act.user_info(request)
        if action == 'ajax':
            return ajax(request)

    except PermissionDenied:    
        #重定向到首页
        return redirect('admin:index')

    return render_to_response(tpl, ctx)

###  admin.user ###
"""
TODO:定制用户表（django.contib.auth.models.AbstractBaseUser)
"""
class UserAct():

    def __init__(self):
        pass

    def user_add(self, request):
        """
        添加user
        表单/处理逻辑
        TODO: 表单自动验证,获取cleandate
        """
        # 显示录入表单（检测 dosubmit字段。若为空则显示录入表单）
        group_list = Group.objects.all().values()
        if  'do_submit' not in request.POST or not post(request, 'do_submit'):
            # 获取group 
            form = UserForm({'is_active':1})
            #print(dir(request.session))
            tpl, ctx = ('admin/user_add.html', {'form': form, 
                                                'group_list': group_list,
                                                'user':request.user,
                                                'action_title':'添加用户'})
        else: #处理提交后的数据
            username = post(request, 'username')
            password = post(request,'password')
            isactive = post(request,'is_active')
            isstaff = post(request,'is_staff')
            firstname = post(request, 'first_name')
            if isactive:
                isactive = 1
            if isstaff:
                isstaff = 1
            try:
                # 验证数据
                uInfo = {'username':username, 'password':password,
                         'first_name':firstname, 'is_staff':isstaff,
                         'is_active':isactive}
                uForm = UserForm(uInfo)
                if(uForm.is_valid()):
                    u = User.objects.create_user(username=username, password=password)
                    u.is_active = 1
                    u.is_staff  = 1
                    u.is_superuser = int(post(request, 'is_superuser'))
                    u.first_name= firstname
                    u.save()
                    # 若上面添加没有出错才会执行到这里
                    # raw 添加 user_group 相应条目
                    # 检查有无group_id post过来

                    if 'group_ids' in request.POST and request.POST['group_ids']:
                        group_ids = request.POST.getlist('group_ids')
                        if group_ids :
                            u.groups = group_ids;
                            u.groups.add()
                           # print(rs)
                    tpl, ctx = ('admin/msg.html', {'title':'提示', 
                                              'content':'添加用户成功！'})
                else:
                    tpl, ctx = ('admin/user_add.html', 
                                {'is_error':'error', 'form':uForm,
                                'group_list': group_list,
                                'content':uForm.errors.as_json()})

            except IntegrityError: #XXX: forms.py 里面进行错误控制self.add_error()之后，这里可能就没用了。
                tpl, ctx = ('admin/msg.html', {'title':'错误', 
                                              'content':'用户名已存在！请选择其他用户名'})

        return (tpl, ctx)

    def user_edit(self, request):
        """
        编辑内容
        """
        group_list = Group.objects.all().values()
        uId = get(request, 'uid')
        if not int(uId):
            tpl, ctx = ('admin/msg.html', {'title':'错误', 
                        'content':'用户不存在，或系统错误！'})

        if request.method != 'POST':
            # 根据uid 获取用户信息
            try:
                oUser = User.objects.get(id=uId)
                u_data = dict(username=oUser.username,
                              first_name=oUser.first_name,
                              is_staff=oUser.is_staff)
                form  = UserForm(initial = u_data) # Fixit
                form.is_valid()
                # 取得当前grouplist
                import sqlite3
                from Ycms.settings import BASE_DIR
                conn = sqlite3.connect(os.path.join(BASE_DIR,'db.sqlite3'))
                # print(os.path.join(BASE_DIR,'db.sqlite3'))
                csr = conn.cursor()
                rs = csr.execute('select group_id from auth_user_groups where user_id = {0}'.format(uId) )
                conn.commit()
                #print('select group_id from auth_user_groups where user_id = {0}'.format(uId) )

                c_g_list = []
                g_id_all = csr.fetchall()
                for g_id in g_id_all:
                    if g_id:
                        c_g_list.append(g_id[0])
                tpl, ctx = ('admin/user_edit.html', {'form': form,
                                                     'oUser': oUser,
                                                     'group_list': group_list,
                                                     'current_group_list': c_g_list,
                                                     'id':uId})
            except :
                tpl, ctx = ('admin/msg.html', {'title':'错误', 'content':'用户不存在！[id 错误]'})

        else:
            # 处理修改
            oUser = User()
            try:
                oUser.first_name = post(request, 'first_name')
                password = post(request, 'password')
                if not password:
                    User.objects.filter(id=post(request,'uid')).update(
                        first_name=post(request, 'first_name'),
                        is_superuser = int(post(request, 'is_superuser'))
                    )
                elif not re.match(re.compile(r'^[^\u4e00-\u9fa5a]{6,16}$'), password):
                    return 'admin/msg.html',{'title':'错误','content':'密码为非中文的6到16位字符'}
                else:
                    pwd = make_password(password)

                    User.objects.filter(id=post(request,'uid')).update(
                        first_name=post(request, 'first_name'),
                        password = pwd,
                        is_superuser = int(post(request, 'is_superuser'))
                    )
                
                # 检查有无group_id post过来

                if 'group_ids' in request.POST and request.POST['group_ids']:
                    group_ids = request.POST.getlist('group_ids')
                    if group_ids :
                        # print(group_ids)
                        # 构造sql
                        str_sql = 'insert into auth_user_groups(user_id, group_id) values '
                        for g_id in group_ids:
                            str_sql = str_sql + '(' + str(uId) + ',' + str(g_id) + '),'
                        str_sql = str_sql.strip(',')
                        # print(str_sql)
                        # 入库
                        import sqlite3
                        from Ycms.settings import BASE_DIR
                        conn = sqlite3.connect(os.path.join(BASE_DIR,'db.sqlite3'))
                        # print(os.path.join(BASE_DIR,'db.sqlite3'))
                        csr = conn.cursor()
                        csr.execute('delete from auth_user_groups where user_id={0}'.format(uId))
                        conn.commit()
                        rs = csr.execute(str_sql)
                        conn.commit()
                        # print(rs)
                tpl, ctx = ('admin/msg.html', {'title':'提示',
                                               'content':'修改成功！'})
            except:
                #pass
                tpl, ctx = ('admin/msg.html', {'title':'错误',
                                               'content':'修改用户出错！'})
                raise
        return (tpl, ctx)

    def user_firbid(self, request):
        uid = max(int(get(request, 'uid')), 0)
        if not uid:
            rtn = 'admin/msg.html', {'title':'错误', 'content':'操作失败[id 非法]！'}
        else:
            # 修改字段
            if User.objects.filter(id=uid).update(is_staff=0):
                rtn = 'admin/msg.html', {'title':'提示', 'content':'操作成功！'}
            else:
                rtn = 'admin/msg.html', {'title':'错误', 'content':'操作失败[无法操作数据库]！'}

        return rtn

    def user_active(self, request):
        uid = max(int(get(request, 'uid')), 0)
        if not uid:
            rtn = 'admin/msg.html', {'title':'错误', 'content':'操作失败[id 非法]！'}
        else:
            # 修改字段
            if User.objects.filter(id=uid).update(is_staff=1):
                rtn = 'admin/msg.html', {'title':'提示', 'content':'操作成功！'}
            else:
                rtn = 'admin/msg.html', {'title':'错误', 'content':'操作失败[无法操作数据库]！'}

        return rtn
        
    def user_list(slef, request):
        """
        user 列表展示
        参数：
            pn 当前page number
        """
        pn =  abs(int(post(request, 'pn'))) or 1
        #print(pn)
        ppn = 'pn' in request.POST and request.POST['pn']
        # 分页参数
        p_size = 20
        item_total = User.objects.count()
        p_total = math.ceil(item_total/p_size) 
        pn = min(p_total, pn)
        p_next = min(p_total, pn + 1)
        p_prev = max(1, pn - 1)
        # 当页内容
        start = p_size * (pn - 1)
        end   = p_size + start
        rs = User.objects.all()[start:end]
        p_list = [p for p in range(1, p_total + 1)]
        ctx = {'pn': pn, 'ppn':ppn, 'p_next':p_next, 'p_prev':p_prev, 'p_total':p_total,
               'p_list':p_list,'rs': rs}
        return ('admin/user.html', ctx)
        
        #pass
        
    def user_del(slef, request):
        """
        删除指定id序列的用户
        ** 注意：这个是彻底删除
        """
        slef.user_firbid(self, request)

    def user_info(self, request):
        try:
            uid = int(get(request, 'uid'))
            oUser = User.objects.get(id=uid)
            oGroups = oUser.groups.all()
            #print(dir(oUser))
            #print(oGroups)
            return 'admin/user-info.html', {'groupList':oGroups,'oUser':oUser}
        except:
            #raise
            return 'admin/msg.html', {'title':'错误',
                                      'content':'用户不存在！'}
            


    def user_recycle(slef, request):
        """
        调用 user_update(_id=(0,), {'status':0}
        设置要放入回收站的 _id 列表中的所有条目（用户） 
        """
        pass

########## 私有方法 ################
    def _user_update(self, id, **keywd):
        """
        私有方法：修改某个字段
        """
        uid = max(id, 0)
        if not uid:
            rtn = 'admin/msg.html', {'title':'错误', 'content':'操作失败[id 非法]！'}
        else:
            # 修改字段
            #print(keywd)
            if(User.objects.filter(id=id).update(keywd)):
                rtn = 'admin/msg.html', {'title':'提示', 'content':'操作成功！'}
            else:
                rtn = 'admin/msg.html', {'title':'错误', 'content':'操作失败[无法操作数据库]！'}
        #print(rtn) 
        return rtn

###  admin.group ###
###  admin.premission ###
###  admin.archive ###
###  admin.sys ###
###  admin.tools ###

