#from django.db import models
#from cmsadmin.mymodels import   *
# Create your models here.
from django.db import models
from django.contrib.auth.models import User, Group, Permission, ContentType

class UserGet:

    def all_as_option(display='first_name'):

        o_user = User.objects.values()
        opt = []
        if o_user:
            for user in o_user:
                _id = user['id']
                f_name = user['first_name']
                opt.append('<option value="{0}">{1}</option>'.format(
                                                                    _id, 
                                                                    f_name)
                            )
        return opt

        

class AuthActions(object):
    """
    获取格式化的权限列表
    { 'content_type.app_label':{
                                    'content_type.model':[
                                                            perm1, 
                                                            perm2, 
                                                            perm3,
                                                            ...
                                                            permN
                                                        ]
     ... ...
    }
    """
    def get_perm_list_tree(ctype=0):
        """
        按ctype id 获取permissions 列表的html code 【checkboxlist】
        """
        # 按ctype 读取Permissions 若ctype 为0则读取全部
        if ctype :
            ctype = int(ctype)
        if ctype:
            perms = Permission.objects.filter(content_type_id = ctype).order_by('content_type')
        else:
            perms = Permission.objects.all().order_by('content_type')

        if not perms:
            return None
        content_types = ContentType.objects.all()
        if not content_types:
            return None
        
        perm_list = {}
        
        # 获取不重复的 app_label
        for ctype in content_types:
            if ctype.app_label not in perm_list:
                perm_list[ctype.app_label] = {'app_label': ctype.app_label, 'models':{}}
        #print(perm_list)        
        for ctype in content_types:
                perm_list[ctype.app_label]['models'][ctype.model]=[]
        for perm in perms:
            try:
                #print(perm)
                perm_list[perm.content_type.app_label]['models'][perm.content_type.model].append(perm)
            except:
                pass

        return perm_list;
