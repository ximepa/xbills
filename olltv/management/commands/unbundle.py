__author__ = 'ximepa'
from django.core.management.base import BaseCommand, CommandError
from core.models import Iptv, Bill, AdminLog, ip_to_num, Tp
import datetime
import calendar
from olltv.api import olltv_auth, oll_disable_bundle


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        auth = olltv_auth()
        iptv_disabled = Iptv.objects.filter(disable=0)
        for iptv in iptv_disabled:
            bill = Bill.objects.get(uid=iptv.uid.id)
            if bill.deposit < 0 and bill.deposit < (iptv.uid.credit * -1) and iptv.disable == 0:
                tp = Tp.objects.get(module='Iptv', tp_id=iptv.tp_id)
                oll_unbundle = oll_disable_bundle(account=iptv.uid.id, sub_id=tp.name, type='subs_negative_balance', hash=auth['hash'])
                print '=========='
                print 'uid: ' + str(iptv.uid.id)
                print 'credit: ' + str(iptv.uid.credit)
                print 'deposit: ' + str(bill.deposit)
                print '=========='
                iptv.disable = 1
                admin_log = AdminLog(
                    actions='Unbundle tarif plan %s' % (tp.name,),
                    datetime=datetime.datetime.now(),
                    ip=ip_to_num('127.0.0.1'),
                    user_id=iptv.uid.id,
                    admin_id='1',
                    action_type=15,
                    module='Iptv',
                )

                iptv.save()
                admin_log.save()
                self.stdout.write('Successfully unbundle')