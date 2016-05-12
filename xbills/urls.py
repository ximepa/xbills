from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
import os
from core.module_check import check

urlpatterns = [
    url(r'^admin/', include('core.urls')),
    url(r'^admin/telephone/', include('telephone.urls')),
    #url(r'^admin/olltv/', include('olltv.urls')),
    #url(r'^admin/', include(admin.site.urls)),
]

if check('olltv'):
    urlpatterns += url(r'^admin/olltv/', include('olltv.urls')),

print urlpatterns