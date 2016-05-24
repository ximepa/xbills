# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'ipdhcp'

urlpatterns = [
    url(r'^$', views.dhcps, name='dhcps'),
    url(r'^(?P<uid>.+)$', views.user_dhcp, name='user_dhcp'),
]