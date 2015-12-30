from django.contrib.auth.models import User
from django.db import models

class Archive(models.Model):
    """
    文章模型主表
    """
    cate_id = models.IntegerField()
    title = models.CharField(max_length=60)
    author_id = models.PositiveSmallIntegerField()
    summary = models.TextField()
    content = models.TextField()
    create_time = models.DatetimeField()
    last_edit_time = models.DatetimeField(auto_now=True)
    # 99：正常 0：垃圾箱 1：草稿
    status = models.PositiveSmallIntegerField()
    # 类似广告为
    position_id = models.PositiveSmallIntegerField()

class Position(models.Model):
    """
    自定义广告位/推荐位
    置顶等状态
    """
    name = models.CharField()
    
class Categary(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=60)
    parent_id = models.PositiveSmallIntegerField()
    # 逗号分割的子id字符串
    children_ids = models.CharFiled(max_length=60)
    # 目录所在层级（深度）
    depth = models.PositiveSmallIntegerField()
        
    ###### 定义操作方法 ########

    def get_parent(self, cid):
        """
        取得父类（所有信息）
        """
        pass

    def get_son(self, cid):
        """
        取得子类
        """
        pass

    def get_all_posterity(self, cid):
        """
        取得所有后代
        """
        pass

    def get_tree(self, cid, leader=' '):
        """
        取得子目录树
        """
        pass


class Author(models.Model):
    pass

