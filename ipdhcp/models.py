from django.db import models
from core.models import User

class Dhcphosts_networks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    network = models.IntegerField(default=0)
    mask = models.IntegerField(default=4294967294)
    routers = models.IntegerField()
    dns = models.CharField(max_length=100)
    dns2 = models.CharField(max_length=100)
    comments = models.CharField(max_length=250)
    ip_range_first = models.IntegerField(default=0)
    ip_range_last = models.IntegerField(default=0)

    class Meta:
        db_table = 'dhcphosts_networks'

    def __unicode__(self):
        return str(self.id)



class Dhcphosts_hosts(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    ip = models.IntegerField()
    hostname = models.CharField(max_length=40)
    network = models.SmallIntegerField()
    mac = models.CharField(max_length=17, default='00.00.00.00.00.00')
    disable = models.SmallIntegerField(default=0)
    vid = models.SmallIntegerField(default=0)
    nas = models.SmallIntegerField(default=0)
    server_vid = models.SmallIntegerField(default=0)

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