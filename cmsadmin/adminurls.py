from django.conf.urls import include, url
from cmsadmin.views import index
from cmsadmin.views import archive
from cmsadmin.views import sysInfo
from cmsadmin.views import user
from cmsadmin.views import group
from cmsadmin.views import tools
from cmsadmin.views import permission
from cmsadmin.views import category
from cmsadmin.views import position
from cmsadmin.views import menu
"""
关于url规则：
    /manage/{module}/{action}
    加
    POST 方法（所有参数都通过post传递，必要时使用js执行传递）
    =====================================
    module: eg. archive/sys/user/group/tools/
    action: eg. create/update/get(read)/del/ajax/import/export
"""
urlpatterns = [
    url(r'^$', index.idx, name = 'index'),
    url(r'^summary/$', index.summary, name = 'summary'),
    url(r'archive/(?P<action>\w+)/$', archive.main, name = 'archive_act'),
    url(r'cate/(?P<action>\w+)/$', category.main, name = 'category_act'),
    url(r'sysinfo/(?P<action>\w+)/$', sysInfo.main, name = 'sysInfo_act'),
    url(r'group/(?P<action>\w+)/$', group.main, name = 'group_act'),
    url(r'user/(?P<action>\w+)/$', user.main, name = 'user_act'),
    url(r'menu/(?P<action>\w+)/$', menu.main, name = 'menu_act'),
    url(r'position/(?P<action>\w+)/$', position.main, name = 'position_act'),
    url(r'permission/(?P<action>\w+)/$', permission.main, name = 'permission_act'),
    url(r'tools/(?P<action>\S+)/$', tools.main, name = 'tools_act'),
]
# 小发现 # url(r'sys/(\w+)/[(\d{0,2})/]*$', sys.main, name = 'sys'),#类似这种情况 可能页面不出错但是 view 函数中无法捕捉到 后面的 []*中的内容
