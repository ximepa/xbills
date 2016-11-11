from core.views import monitoring_servers
from voip.call import hangup

__author__ = 'ximepa'
from django.conf.urls import url
from . import views
from .helpers import module_check

app_name = 'core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^get_pc_info/$', get_responses, name='get_pc_info'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^hangup/$', hangup, name='hangup'),
    url(r'^monitoring_servers/$', monitoring_servers, name='monitoring_servers'),
    url(r'^clients/$', views.clients, name='clients'),
    url(r'^clients/(?P<uid>\d+)/$', views.client, name='client'),
    url(r'^search/$', views.search, name='search'),
    url(r'^test/$', views.test, name='test'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    #url(r'^search/$', views.search, name='search'),
    #url(r'^users/$', views.users, name='users'),
    url(r'^payments/$', views.payments, name='payments'),
    url(r'^fees/$', views.fees, name='fees'),
    url(r'^company/$', views.company, name='company'),
    url(r'^group/$', views.group, name='group'),
    url(r'^settings/administrators/$', views.administrators, name='administrators'),
    url(r'^settings/administrators_add/$', views.administrators_add, name='administrators_add'),
    url(r'^settings/administrators/(?P<uid>\d+)/$', views.administrator_edit, name='administrator_edit'),
    url(r'^settings/servers/$', views.servers, name='servers'),
    url(r'^settings/tarif_plans/$', views.tarif_plans, name='tarif_plans'),
    url(r'^clients/(?P<uid>\d+)/payments/$', views.client_payments, name='client_payments'),
    url(r'^clients/(?P<uid>\d+)/fees/$', views.client_fees, name='client_fees'),
    url(r'^clients/(?P<uid>\d+)/group/$', views.user_group, name='user_group'),
    url(r'^clients/(?P<uid>\d+)/company/$', views.user_company, name='user_company'),
    url(r'^clients/(?P<uid>\d+)/errors/$', views.client_errors, name='client_errors'),
    url(r'^clients/(?P<uid>\d+)/statistics/$', views.client_statistics, name='client_statistics'),
]

if module_check('ipdhcp'):
    try:
        from ipdhcp import views as ipdhcp_views
    except:
        pass
    finally:
        urlpatterns += url(r'^clients/(?P<uid>.+)/dhcp/$', ipdhcp_views.user_dhcp, name='user_dhcp'),
        urlpatterns += url(r'^clients/(?P<uid>.+)/dhcp/(?P<host_id>.+)/$', ipdhcp_views.user_dhcp, name='user_ipdhcp_host_change'),
if module_check('claims'):
    try:
        from claims import views as claims_views
    except:
        pass
    finally:
        urlpatterns += url(r'^clients/(?P<uid>\d+)/claims/$', claims_views.user_claims, name='user_claims'),
