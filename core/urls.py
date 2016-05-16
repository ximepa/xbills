__author__ = 'ximepa'
from django.conf.urls import patterns, url
from . import views
app_name = 'core'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^clients/$', views.clients, name='clients'),
    url(r'^clients/(?P<uid>\d+)/$', views.client, name='client'),
    url(r'^search/$', views.search, name='search'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    #url(r'^search/$', views.search, name='search'),
    #url(r'^users/$', views.users, name='users'),
    url(r'^payments/$', views.payments, name='payments'),
    url(r'^fees/$', views.fees, name='fees'),
    url(r'^settings/administrators/$', views.administrators, name='administrators'),
    url(r'^settings/nas/$', views.nas, name='nas'),
    url(r'^payments/(?P<uid>\d+)/$', views.client_payments, name='client_payments'),
    url(r'^fees/(?P<uid>\d+)/$', views.client_fees, name='client_fees'),
    url(r'^clients/(?P<uid>\d+)/group/$', views.user_group, name='user_group'),
    url(r'^clients/(?P<uid>\d+)/company/$', views.user_company, name='user_company'),
    url(r'^clients/(?P<uid>\d+)/errors/$', views.client_errors, name='client_errors'),
    url(r'^clients/(?P<uid>\d+)/statistics/$', views.client_statistics, name='client_statistics'),
    url(r'^static_pools$', views.static_pools, name='static_pools'),
]