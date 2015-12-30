from django.contrib.auth.models import User

"""
appadmin 的model
"""

###  admin.user ###
"""

TODO:定制用户表（django.contib.auth.models.AbstractBaseUser)
"""
def user_add(**key_val):
    """
    添加user
    表单/处理逻辑
    """
    #检查key_val合法性


def user_update(_id=(0,), *key_val):
    """
    user 数据表字段修改
    回收站/user等级等等
    _id: 0 --无任何操作
         num --相应要改的id元组
    *key_val: 字典。
              {'字段名':'值'}

    TODO: 多条记录批量修改
    """
    pass

def user_list(user_type=9):
    """
    user 列表展示
    user_type : 99--超级管理员(权限组无法控制）
                1 --普通用户（可用权限组控制）
    """
    pass
    
def user_del(_id=(0,)):
    """
    删除指定id序列的用户
    ** 注意：这个是彻底删除
    """
    pass

def user_recycle(_id=(0,)):
    """
    调用 user_update(_id=(0,), {'status':0}
    设置要放入回收站的 _id 列表中的所有条目（用户） 
    """
    pass

###  admin.group ###
###  admin.premission ###
###  admin.archive ###
###  admin.sys ###
###  admin.tools ###

