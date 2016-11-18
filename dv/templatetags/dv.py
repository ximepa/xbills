import datetime
import binascii
from django import template
import math
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from core.models import num_to_ip, Admin, User, Tp, Dv_calls
from django.conf import settings
import os

register = template.Library()

@register.inclusion_tag('sessions.html')
def session(uid):
    try:
        dv_session = Dv_calls.objects.values(
            'framed_ip_address',
            'started',
            'acct_input_octets',
            'acct_input_gigawords',
            'acct_output_octets',
            'acct_output_gigawords',
            'nas__name',
            'acct_session_id',
            'nas__id',
            'nas_port_id',
            'user_name',
        ).filter(uid=uid)
        # return dv_session
        return {'dv_session' : dv_session}
    except Dv_calls.DoesNotExist:
        return None