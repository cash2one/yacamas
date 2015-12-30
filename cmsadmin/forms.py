from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission
from appcms.models import Archive, Category
import re

"""
定义后台的form
利用django自身的form类来生成表单
并且可通过其进行字段验证等
"""
class CateForm(ModelForm):

    def clean(self):
        cleaned_data = super(CateForm, self).clean()
        alias = cleaned_data.get('alias')
        name = cleaned_data.get('name')
       # if not re.match(re.compile(r'^[ \-a-zA-Z\d]+$'), alias):
       #     self.add_error('alias',
       #                   '别名不能为空，且只能使用大小写字母和数字')
    class Meta:
        model = Category
        fields = ['alias', 'name', 'cate_type']

class UserForm(ModelForm):
    """
    用户系统 user模块的form
    """
    def clean(self):
        """
        form提交数据预处理
            > 有效性
            > 字段额外规则定义及验证
        """
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        #用户名不能为中文
        if  not re.match(re.compile(r'^[\S\d_]{1,99}$'), username):
            self.add_error('username', '用户名仅能为英文字母/数字/下划线！')
            
        if password and not re.match(re.compile(r'^[^\u4e00-\u9fa5a]{6,16}$'), password):
            self.add_error('password', '密码为6-16位“非中文“字符！')

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff']
    

class GroupForm(ModelForm):

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        name = cleaned_data.get('name')

        # name 只能是中文或英文/数字 且不能以数字开头
        if not re.match(re.compile(r'^[\S\u4e00-\u9fa5a_][\S\u4e00-\u9fa5a_\d]{1,29}$'), name):
            self.add_error('name', '组名称只能是【英文/汉字/数字/_】的组合，且不能以数字开头')

    class Meta:
        model = Group
        fields = ['name']

class ArchiveForm(ModelForm):
    def clean(self):
        cleaned_data = super(ArchiveForm, self).clean()
        cate_id = cleaned_data.get('cate_id')
        content = cleaned_data.get('content')
        title = cleaned_data.get('title')
        #过滤script
        for key in cleaned_data:
            val = cleaned_data[key]
            if isinstance(val, str):
                cleaned_data[key] = val.replace('<script', '< script')
        
        # cate_id
        if cate_id < 0:
            self.add_error('cate_id', '请先选择分类！')


        # title
        if title and len(title.replace(' ', '')) < 2:
            self.add_error('title', '标题太短！')




    class Meta:
        model = Archive
        fields = ['title', 
                  'keywords', 
                  'description', 
                  'referer',
                  'content',
                  'summary',
                  'cate_id',
                  'author',
                  'create_time',
                 #'last_edit_time',
                  'position_id',
                ]

class PermissionForm(ModelForm):

    class META:
        model = Permission
        fields = ['code_name', 'name', 'content_type_id']

class SysForm(ModelForm):
    pass

class ToolsForm(ModelForm):
    pass


