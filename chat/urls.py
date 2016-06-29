# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from django.core.urlresolvers import reverse_lazy
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.contrib import admin
from .views import BroadcastChatView, UserChatView, GroupChatView, BroadcastChatAdminView
admin.autodiscover()
app_name = 'chat'


urlpatterns = [
    url(r'^$', BroadcastChatView.as_view(), name='broadcast_chat'),
    url(r'^chat_admin/$', BroadcastChatAdminView.as_view(), name='broadcast_chat_admin'),
    url(r'^userchat/$', UserChatView.as_view(), name='user_chat'),
    url(r'^groupchat/$', GroupChatView.as_view(), name='group_chat'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
] + staticfiles_urlpatterns()
