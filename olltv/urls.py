# -*- coding: utf-8 -*-
from django.conf.urls import *
from . import views
app_name = 'olltv'

urlpatterns = [
    # url(r'^add_tp/(?P<uid>.+)/$', views.add_tp, name='add_tp'),
    # url(r'^add_aditional_tp/(?P<uid>.+)/$', 'add_aditional_tp', name='add_aditional_tp'),
    # url(r'^unbundle/(?P<account>.+)/(?P<sub_id>.+)/$', 'unbundle', name='unbundle'),
    # url(r'^unbundle_aditional/(?P<account>.+)/(?P<sub_id>.+)/$', 'unbundle_aditional', name='unbundle_aditional'),
    # url(r'^change_email/(?P<account>.+)/$', 'change_email', name='change_email'),
    # url(r'^change_userinfo/(?P<account>.+)/$', 'change_userinfo', name='change_userinfo'),
    # url(r'^get_all_dev/$', 'get_all_dev', name='get_all_dev'),
    # url(r'^get_all_users/$', 'get_all_users', name='get_all_users'),
    # url(r'^device_add/(?P<account>.+)/$', 'device_add', name='device_add'),
    # url(r'^device_remove/(?P<account>.+)/(?P<mac>.+)/(?P<serial_number>.+)/$', 'device_remove', name='device_remove'),
    #url(r'^user_change/(?P<account>.+)/$', 'user_change', name='user_change'),
    # url(r'^user_add/$', 'user_add', name='user_add'),
    # url(r'^logout/', 'logout_view', name='logout_view'),
    # #url(r'^rpc/', include(rpc_router.urls, 'rpc')),
    # url(r'^(?P<uid>.+)/$', views.user_change, name='user_change'),
    url(r'^olltv/$', views.index, name='index'),
    url(r'^clients/(?P<uid>\d+)/olltv/$', views.user_change, name='user_olltv'),
]