from django.db import models
from core.models import User

class Dhcphosts_networks(models.Model):
    id = models.SmallIntegerField(max_length=3, primary_key=True)
    name = models.CharField(max_length=40)
    network = models.IntegerField(max_length=10, default=0)
    mask = models.IntegerField(max_length=11, default=4294967294)
    routers = models.IntegerField(max_length=11)
    dns = models.CharField(max_length=100)
    dns2 = models.CharField(max_length=100)
    comments = models.CharField(max_length=250)
    ip_range_first = models.IntegerField(max_length=11, default=0)
    ip_range_last = models.IntegerField(max_length=11, default=0)

    class Meta:
        db_table = 'dhcphosts_networks'

    def __unicode__(self):
        return str(self.id)



class Dhcphosts_hosts(models.Model):
    id = models.SmallIntegerField(max_length=3, primary_key=True)
    uid = models.IntegerField(max_length=11)
    ip = models.IntegerField(max_length=10)
    hostname = models.CharField(max_length=40)
    network = models.SmallIntegerField(max_length=5)
    mac = models.CharField(max_length=17, default='00.00.00.00.00.00')
    disable = models.SmallIntegerField(max_length=1, default=0)
    vid = models.SmallIntegerField(max_length=6, default=0)
    nas = models.SmallIntegerField(max_length=6, default=0)
    server_vid = models.SmallIntegerField(max_length=6, default=0)

    class Meta:
        db_table = 'dhcphosts_hosts'

    def __unicode__(self):
        return str(self.id)


def ipRange(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
        ip_range.append(".".join(map(str, temp)))

    return ip_range