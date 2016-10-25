from django.conf.urls import patterns, url
from . import views
app_name = 'api'

urlpatterns = [
    url(r'^districts/$', views.district_view, name='district_view'),
    url(r'^streets/$', views.street_view, name='street_view'),
    url(r'^houses/$', views.house_view, name='house_view'),
]