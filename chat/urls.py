from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
app_name = 'chat'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='chat.html'), name='home'),
]
