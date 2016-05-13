__author__ = 'ximepa'
from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def apiversion():
    try:
        settings.OLLTVAPIVERSION
    except:
        return ''
    return settings.OLLTVAPIVERSION


@register.simple_tag
def version():
    if settings.SHOW_VERSION:
        return str(settings.COMPANY_NAME) + ' ' + str(settings.PROJECT_VERSION)
    else:
        return str(settings.COMPANY_NAME)