__author__ = 'ximepa'
from django.core.management.base import BaseCommand, CommandError
from core.models import Iptv, Bill, AdminLog, ip_to_num, Tp, Fees
import datetime
from olltv.api import olltv_auth, oll_add_bundle
from olltv.commands import make_conversion


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        auth = olltv_auth()
        iptv_disabled = Iptv.objects.filter(disable=1)
        for iptv in iptv_disabled:
            bill = Bill.objects.get(uid=iptv.uid.id)
            tp = Tp.objects.get(tp_id=iptv.tp_id)
            if (bill.deposit + iptv.uid.credit) > make_conversion(tp.cost) and iptv.disable == 1:
                oll_bundle = oll_add_bundle(account=iptv.uid.id, tp=tp.name, type='subs_renew', hash=auth['hash'])
                print '=========='
                print 'account=' + str(iptv.uid.id)
                print 'credit=' + str(iptv.uid.credit)
                print 'deposit=' + str(bill.deposit)
                print 'all_deposit=' + str(bill.deposit + iptv.uid.credit)
                print 'have pay=' + str(make_conversion(tp.cost))
                print '=========='
                iptv.disable = 0
                iptv.registration = datetime.date.today()
                admin_log = AdminLog(
                    actions='bundle tarif plan %s' % (tp.name),
                    datetime=datetime.datetime.now(),
                    ip=ip_to_num('127.0.0.1'),
                    user_id=iptv.uid.id,
                    admin_id='1',
                    action_type=15,
                    module='Iptv',
                )
                iptv.save()
                admin_log.save()
                self.stdout.write('Successfully bundle')