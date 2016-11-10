from django.db import models
from core.models import User
from core.models import num_to_ip
from core.validators import validate_mac

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
        ordering = ['name']
        db_table = 'dhcphosts_networks'

    def __unicode__(self):
        return str(self.id) + ' ' + str(self.name) + ' ' + '(IP: %s, Netmask: %s)' % (num_to_ip(self.network), num_to_ip(self.mask))



class Dhcphosts_hosts(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    ip = models.GenericIPAddressField(default='0.0.0.0')
    hostname = models.CharField(max_length=255, unique=True, blank=False)
    network = models.ForeignKey('Dhcphosts_networks', db_column='network', blank=False)
    mac = models.CharField(max_length=17, default='00:00:00:00:00:00', validators=[validate_mac], unique=True)
    disable = models.BooleanField(default=0, blank=True)
    vid = models.IntegerField(default=0)
    nas = models.IntegerField(default=0)
    server_vid = models.IntegerField(default=0)

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


def new_ip(network_id):
    print network_id
    ip_list = []
    ip_db = Dhcphosts_hosts.objects.filter(network=network_id)
    network = Dhcphosts_networks.objects.get(id=network_id)
    print network.ip_range_first
    print network.ip_range_last
    for ip_range in ip_db:
        ip_list.append(num_to_ip(ip_range.ip))
    print ip_list
    print ipRange(num_to_ip(network.ip_range_first), num_to_ip(network.ip_range_last))
    result = [i for i in ipRange(num_to_ip(network.ip_range_first), num_to_ip(network.ip_range_last)) if i not in ip_list]
    print result[0]
    return result[0]