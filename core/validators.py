from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from netaddr import *
from django.conf import settings
from core.models import User


def validate_mac(value):
    if valid_mac(value):
        value = EUI(value, dialect=mac_unix_expanded)
        # if settings.UNIQUE_MAC == True:
        #     from ipdhcp.models import Dhcphosts_hosts
        #     try:
        #         host = Dhcphosts_hosts.objects.get(mac=value)
        #         raise ValidationError(_('%(value)s binded to user %(user)s'),
        #                               params={'value': value, 'user': host.uid}, )
        #     except Dhcphosts_hosts.DoesNotExist:
        #         return value
        # else:
        return value
    else:
        raise ValidationError(_('%(value)s is not a mac address, or unknown format'), params={'value': value},)
