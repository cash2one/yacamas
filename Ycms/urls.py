from django.conf.urls import include, url
import cmsadmin.adminurls
from cmsadmin.views.index import login, logout
from apppubactions.myviews.filemanage.upload import Controller as upCtrl
import appcms.urls
import appt.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'Ycms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'appcms.views.index', name = 'site_index'),
    url(r'^cms/', include(appcms.urls, namespace='cms')),
    url(r'^manage/', include(cmsadmin.adminurls, namespace='admin')),
    url(r'^login/$', login, name = 'login'),
    url(r'^logout/$', logout, name = 'logout'),
    url(r'^pubact/filemanage/upload/$', upCtrl, name = 'imageup'),
    #url(r'^verfy/$', verfy, name='verfy'), 
    url(r'^t/', include(appt.urls, namespace='appt')),
]
