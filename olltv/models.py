from django.db import models
from django.conf import settings
import datetime
from core.models import User


class IptvDevice(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    uid = models.ForeignKey(User, blank=True, null=True, related_name='devices', related_query_name='dev', db_column='uid')
    device_type = models.ForeignKey('IptvDeviceType', max_length=100, default=1, db_column='device_type')
    mac = models.CharField(max_length=100, default='000000000000')
    serial_num = models.CharField(max_length=100, default='0')
    model = models.CharField(max_length=100, default='0')
    status = models.BooleanField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = 'iptv_devices'
        ordering = ['-id']


class IptvDeviceType(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, default='stb', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'iptv_device_type'
        ordering = ['-id']