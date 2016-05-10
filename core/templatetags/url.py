import datetime
from datetime import datetime
import binascii
from django import template
import math
from core.models import num_to_ip

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    if field == 'order_by' and field in dict_.keys():
        if dict_[field].startswith('-') and dict_[field].lstrip('-') == value:
            dict_[field] = value
        else:
            dict_[field] = "-"+value
    else:
        dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def url_replace_page(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def ip_convert(value):
    return num_to_ip(value)


@register.simple_tag
def convert_timestamp_to_time(timestamp):
    import time
    session_time = datetime.now() - timestamp
    days, seconds = session_time.days, session_time.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return '%s:%s:%s' % (hours, minutes, seconds)


@register.simple_tag
def convert_bytes(value, giga):
    if giga == 0:
        value = value
    else:
        value = value + 4294967296 * giga
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(value,1024)))
    p = math.pow(1024,i)
    s = round(value/p,2)
    return '%s %s' % (s, size_name[i])