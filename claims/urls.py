__author__ = 'ximepa'
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = 'claims'

urlpatterns = [
    url(r'^$', views.index, name='claims'),
    url(r'^claims_list/', views.claims_list, name='claims_list'),
    url(r'^name/', views.name, name='name'),
    url(r'^all/', views.claims_list_all, name='list_all'),
    # url(r'^new/', views.claim_create, name='claim_new'),
    # url(r'^(?P<id>.+)/edit/', views.claim_edit, name='claim_edit'),
    # url(r'^(?P<uid>.+)/edit/state/', views.claim_edit, name='claim_state'),
    # url(r'^(?P<uid>.+)/edit/priority/', views.claim_edit, name='claim_priority'),
    # url(r'^(?P<uid>.+)/edit/queue/', views.claim_edit, name='claim_queue'),
    url(r'^(?P<uid>.+)/delete$', views.claim_delete, name='claim_delete'),
    url(r'^map/(?P<claim_id>.+)/$', views.claim_map, name='claim_map'),
]
