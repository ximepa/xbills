from django.core.management.base import BaseCommand, CommandError
from core.models import User as Client, Company, Bill
import datetime

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # print self
        # print args
        # print options
        # print Company.objects.all()
        client = Client.objects.get(id=5973)
        print client.login
        print client.dv.tp.day_fee
        print client.dv.tp.month_fee
        # print client.company
        print client.bill.id
        today = datetime.datetime.today()
        first_day = datetime.date(today.year, today.month, 1)
        if client.dv.tp.month_fee == 0:
            client.bill.deposit = client.bill.deposit - client.dv.tp.day_fee
            # client.save()
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))