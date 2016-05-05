from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
import os
olltv_module_path = os.path.join(settings.BASE_DIR,  'olltv')
modules = settings.INSTALLED_APPS

urlpatterns = [
    url(r'^admin/', include('core.urls')),
    url(r'^admin/telephone/', include('telephone.urls')),
    #url(r'^admin/olltv/', include('olltv.urls')),
    #url(r'^admin/', include(admin.site.urls)),
]

if 'olltv' in modules and os.path.exists(olltv_module_path):
    urlpatterns += url(r'^admin/olltv/', include('olltv.urls')),

print urlpatterns