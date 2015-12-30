from django.conf.urls import url
from .views import index, session, taba, tabb, tabc

urlpatterns = [
    url('^$', index, name='index'),
    url('^session$', session, name='tsession'),
    url('^taba/$', taba, name='taba'),
    url('^tabb/$', tabb, name='tabb'),
    url('^tabc/$', tabc, name='tabc'),

]
