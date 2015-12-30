from django.conf.urls import url
from .views import main
urlpatterns = [
   # url(r'^(?P<cate_alias>[a-zA-Z\d\-]+)/$', category, name='cate'),
   # url(r'^(?P<cate_alias>[a-zA-Z\d\-]+)/(?P<subcate_alias>[a-zA-Z\d\-]+)/$', 
   #     category, name='cate_with_subcate'),
   # url(r'^(?p<cate_alias>[a-zA-Z\d\-]+)/(?P<archive>[a-zA-Z\d\-]+).do$', 
   #     archive, name='archive'),
   # url(r'^(?P<cate_alias>[a-zA-Z\d\-]+)/(?P<subcate_alias>[a-zA-Z\d\-]+)/(?P<archive>[a-zA-Z\d\-]+)\.do$',
   #    archive, name='archive_with_subcate'),
    
    url(r'^$', main, name='cms_main'),
]
