from django.conf.urls import url
from .views import index, session

urlpartterns = [
    url('^$', index, name='index'),
    url('^index/$', session, name='session'),
]
