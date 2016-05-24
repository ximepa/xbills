# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'iphdcp'

urlpatterns = [
    url(r'^$', views.dhcps, name='dhcps'),
]