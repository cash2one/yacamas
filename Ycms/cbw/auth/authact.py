"""
自定义的用户登录/登出/节点认证
导入：
    #1 User
    #2 Group
    #3 Permission
用户登录：
    #1 过滤表单提交的用户名/密码/验证码
    #2 查询数据库（User）
    #3 验证成功 登入系统
    #4 读取 所属组
    #5 读取 所有组的权限
    #6 用户信息/组信息/权限信息 缓存到session
节点认证：
    #1 user.has_perm(content_type, permission)
    #2 从session中读取权限列表 若有权限则继续，若无权限则跳转（或提示）
"""
import re, math
from django.contrib.auth.models import User, Group, Permission


class YcmsError(Exception):
    pass

class YcmsInvolidUserName(YcmsError):
    """
    用户名非法
    """
    pass



class Yuser(object):
    """
    """
    def get_user_by_name(u_name=''):
        # 验证用户名字符是否合规
        # XXX: sql_filter 防注入过滤 放到 Ycms.functions中
        u_name = sql_filter(u_name).replace(' ', '')
        if re.match(re.compile(r'^$'), u_name):
            # 读取数据库查找用户名是否在系统中
            o_user = User.objects.get(username=u_name)
            if not o_user:
                raise YcmsUserNotExists()
            else:
                return o_user
        else:
            raise YcmsInvolidUserName()

    def login(request, o_user, redirect_url=''):
        """
        用户登录表单/登录验证
        """
        if request.method == 'POST':
            # 处理用户登录验证
            pass
        else:
            # 显示登录表单
            pass

    def logout(request, o_user, redirect_url=''):
        """
        用户登出处理
        """
        # 清空session

        # 跳转
        pass

    def has_perm(perm='', content=''):
        """
        用户认证： 是否有某个权限
        """
        # 获取用户权限列表

        # 查找用户权限列表中有无对应的 content  perm
        
        # 有则返回True 无则返回 False
        pass

    def generate_pwd(pwdstr=''):
        """
        给定pwdstr 加密
        # 需要分析django的加密方法
        """
        pass


