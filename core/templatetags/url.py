import datetime
import binascii
from django import template
import math
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from core.models import num_to_ip, Admin, User, Tp
from django.conf import settings
import os

register = template.Library()


@register.simple_tag
def check_module(module):
    modules = settings.INSTALLED_APPS
    module_path = os.path.join(settings.BASE_DIR, module)
    if module in modules and os.path.exists(module_path):
        return True
    else:
        return False


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    if field == 'order_by' and field in dict_.keys():
        if dict_[field].startswith('-') and dict_[field].lstrip('-') == value:
            dict_[field] = value
        else:
            dict_[field] = "-" + value
    else:
        dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def url_replace_page(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def theme(request, static_file):
    if request.user.pk is not None:
        try:
            user_theme = Admin.objects.get(id=request.user.pk).theme
            return '/static/' + user_theme + static_file
        except:
            return '/static/default/' + static_file
    else:
        return '/static/default/' + static_file


@register.simple_tag
def ip_convert(value):
    return num_to_ip(value)


@register.simple_tag
def convert_timestamp_to_time(timestamp):
    import time
    session_time = datetime.datetime.now() - timestamp
    days, seconds = session_time.days, session_time.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return '%s:%s:%s' % (hours, minutes, seconds)


@register.simple_tag
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


@register.simple_tag
def sizify(value):
    if value < 512000:
        value = value / 1024.0
        ext = 'KB'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'MB'
    else:
        value = value / 1073741824.0
        ext = 'GB'
    return '%s %s' % (str(round(value, 2)), ext)


@register.simple_tag
def convert_bytes(value, giga):
    # print value
    # print giga
    if value != 0:
        if giga == 0:
            value = value
        else:
            value += 4294967296 * giga
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(value, 1024)))
        p = math.pow(1024, i)
        s = round(value / p, 2)
        return '%s %s' % (s, size_name[i])
    else:
        print value
        return '%s %s' % (str(value), 'B')


@register.simple_tag
def active(request, url, *args):
    if request.path == (reverse(url, args=args)):
        return 'active'
    return ''


@register.simple_tag
def active_startwith(request, url, *args):
    if request.path.startswith(reverse(url)):
        return 'active'
    return ''


@register.simple_tag
def user_company(id):
    user_count = User.objects.filter(company_id=id).count()
    return user_count


@register.simple_tag
def user_group(id):
    user_group = User.objects.filter(gid=id).count()
    return user_group


@register.simple_tag
def status(value):
    if value != None:
        stat = 'Enable'
    else:
        stat = 'Disable'
    return stat

@register.simple_tag
def sec_to_time(sec):
    return str(datetime.timedelta(seconds=sec))

@register.simple_tag
def tp_name(id):
    name = Tp.objects.get(id=id)
    return name.name

@register.simple_tag
def pay_type(id):
    type = ''
    if id == 0: type = _('Cash')
    elif id == 1: type = _('Bank')
    elif id == 2: type = _('External Payments')
    elif id == 3: type = ''
    elif id == 4: type = _('Bonus')
    return type