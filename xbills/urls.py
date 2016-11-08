from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import os
from core.helpers import module_check
from core.rpc import rpc_router

urlpatterns = [
    url(r'^api/', include('api.urls', 'api')),
    url(r'^admin/', include('core.urls')),
    url(r'^admin/telephone/', include('telephone.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^rpc/', include(rpc_router.urls, 'rpc')),
]
if module_check('ipdhcp'):
    urlpatterns += url(r'^admin/dhcps/', include('ipdhcp.urls')),
if module_check('olltv'):
    urlpatterns += url(r'^admin/', include('olltv.urls', 'olltv')),
if module_check('claims'):
    urlpatterns += url(r'^admin/claims/', include('claims.urls')),
if module_check('chat'):
    urlpatterns += url(r'^admin/chat/', include('chat.urls')),
else:
    urlpatterns += url(r'^admin/chat/', TemplateView.as_view(template_name='404.html'), name='home'),

