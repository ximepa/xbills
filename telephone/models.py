from __future__ import unicode_literals
from django.db import models
from core.models import Street, District, House
from django.core.urlresolvers import reverse
from django.core import exceptions
from django.db import router


class Client(models.Model):
    fio = models.CharField(max_length=1000)
    district = models.ForeignKey(District)
    street = models.ForeignKey(Street)
    house = models.ForeignKey(House)
    kv = models.CharField(max_length=50)
    deposit = models.FloatField(default=0.0)
    ur = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id) + ':' + self.fio