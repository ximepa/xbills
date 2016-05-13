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
    header = ''
    if hasattr(settings, 'COMPANY_NAME'):
        header += settings.COMPANY_NAME
    if hasattr(settings, 'SHOW_VERSION'):
        if hasattr(settings, 'COMPANY_NAME'):
            return header + ' ' + str(settings.PROJECT_VERSION)
        else:
            return str(settings.PROJECT_VERSION)
    else:
        return header