from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import os
from core.helpers import module_check

urlpatterns = [
    url(r'^admin/', include('core.urls')),
    url(r'^admin/telephone/', include('telephone.urls')),

    #url(r'^admin/olltv/', include('olltv.urls')),
    #url(r'^admin/', include(admin.site.urls)),
]
if module_check('ipdhcp'):
    urlpatterns += url(r'^admin/dhcps/', include('ipdhcp.urls')),
if module_check('olltv'):
    urlpatterns += url(r'^admin/olltv/', include('olltv.urls')),
if module_check('claims'):
    urlpatterns += url(r'^admin/claims/', include('claims.urls')),
if module_check('chat'):
    urlpatterns += url(r'^admin/chat/', include('chat.urls')),

