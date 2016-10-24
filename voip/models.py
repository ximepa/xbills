from django.db import models


class AsteriskCall(models.Model):

    uniqueid = models.CharField(max_length=100)
    caller_num = models.CharField(max_length=45)
    destination_num = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    start_call = models.DateTimeField()

    def __unicode__(self):
        return self.caller_num

    class Meta:
        db_table = 'asterisk_calls'
        ordering = ['caller_num']