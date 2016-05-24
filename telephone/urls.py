__author__ = 'ximepa'
from django.conf.urls import patterns, url
from . import views
app_name = 'telephone'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^clients/$', views.clients, name='clients'),
    # url(r'^users/(?P<id>\d+)/group/$', views.user_group, name='user_group'),
    # url(r'^users/(?P<id>\d+)/company/$', views.user_company, name='user_company'),
]