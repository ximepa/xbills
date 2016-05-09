import datetime
from datetime import datetime
from django import template
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
    print timestamp
    print datetime.now()
    session_time = datetime.now() - timestamp
    return str(session_time)