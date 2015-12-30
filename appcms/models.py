from django.contrib.auth.models import User
from django.db import models

class Archive(models.Model):
    """
    文章模型主表
    """
    cate_id = models.IntegerField()
    title = models.CharField(max_length=60,default='')
    author = models.CharField(max_length=30,default='')
    summary = models.TextField(blank=True)
    content = models.TextField()
    keywords= models.CharField(max_length=100,blank=True,default='')
    description = models.CharField(max_length=100,blank=True,default='')
    referer = models.CharField(max_length=100,blank=True,default='')
    tpl = models.CharField(max_length=50, default='')
    create_time = models.DateTimeField()
    last_edit_time = models.DateTimeField(auto_now=True)
    # 类似广告位
    position_id = models.CharField(max_length=60, blank=True, default='0')
    # 99：正常 0：垃圾箱 1：草稿
    status = models.PositiveSmallIntegerField(default=99)
    
    class Meta:
        permissions = (
                ('add_arch','添加文章'),
                ('edit_arch','编辑文章'),
                ('get_arch','读取文章'),
                ('del_arch','删除文章'),
            )


class Position(models.Model):
    """
    自定义广告位/推荐位
    置顶等状态
    """
    name = models.CharField(max_length=60)
    
    def get_all_as_checkbox():
        rs = Position.objects.values()
        pos_list = []
        if rs :
            for pos in rs:
                pos_list.append('<input type="checkbox" name="position_id" \
                                value="{0}" class="position" /> \
                                {1}'.format(pos['id'], pos['name']))
        return pos_list
    
class Category(models.Model):
    """
    分
    """
    SIGLE_PAGE = 'SINGLE'
    NORMAL_CATE= 'NORMAL'
    CATE_TYPE = (
        (SIGLE_PAGE, '单页面分类'),
        (NORMAL_CATE, '常规分类'),
    )
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    pid = models.PositiveSmallIntegerField()
    # 逗号分割的子id字符串
    path = models.CharField(max_length=60)
    list_order = models.PositiveSmallIntegerField(default=0)
    cate_type = models.CharField(max_length=6, 
                                 choices=CATE_TYPE,
                                 default=NORMAL_CATE)
    has_child = models.BooleanField()
    description = models.TextField()
    status = models.PositiveSmallIntegerField(default=99)
    # 目录所在层级（深度）
    depth = models.PositiveSmallIntegerField()

        
    ###### 定义操作方法 ########
    #  model 里面定义的方法无法调用！！？？ 
    # 提示： 缺少参数self
    #
    def get_cate_by_id(cid=0):

        if not cid:
            return False

        # 查数据库
        cate = Category.objects.get(id=cid).values()
    
    def get_all_as_dict(cid=0):
        """
        取得所有后代
        """
        return Category.objects.values()

    def get_tree_as_options(cid=0):
        """
        取得子目录树
        """
        from Ycms.tree import CategoryTree
        cate_list = Category.objects.values()
        o_tree = CategoryTree(cate_list)
        return o_tree.tree(cid=cid, seprator=' .&nbsp; ', 
                           wrapper='<option value="{2}">{0}</option>',
                           wrapper_all=True)
class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=60, default='')
    url  = models.CharField(max_length=260, default='')
    m_type = models.CharField(max_length=10, default='back')
    code = models.CharField(max_length=30, default='')
    list_order = models.PositiveSmallIntegerField(default=0)
    perm_id = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=99)
    pid = models.PositiveSmallIntegerField()
    # 逗号分割的子id字符串
    path = models.CharField(max_length=60)
    has_child = models.BooleanField()
    # 目录所在层级（深度）
    depth = models.PositiveSmallIntegerField()
                
        

class Author(models.Model):
    pass

class SysInfo(models.Model):
    """
    系统信息
    """
    key = models.CharField(max_length=60, default='', unique=True)
    value = models.CharField(max_length=5000, default='')

