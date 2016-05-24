from django.db import models

class Dhcphosts_networks(models.Model):
    id = models.SmallIntegerField(max_length=3, primary_key=True)
    name = models.CharField(max_length=40)
    network = models.IntegerField(max_length=10, default=0)
    mask = models.IntegerField(max_length=11, default=4294967294)

    class Meta:
        db_table = 'dhcphosts_networks'

    def __unicode__(self):
        return str(self.id)