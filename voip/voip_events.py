import json
import logging
import re
from django.db.models import Q
from core.models import UserPi
from django.http import HttpResponse
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


extensions={"SIP/72":"monitoring"}
log = logging.getLogger( 'hellofastagi' )


def kill_4744(value):
    num = re.findall(r'^4744(\d{5})', value)
    if num:
        return num[0]
    else:
        return value

class VoipEvents:
    servers = {}
    def __init__(self):
        # log.log(logging.NOTICE, "Initializing Monast AMI Interface...")

        self.eventHandlers = {
            'Hangup'              : self.handlerEventHangup,
			'Dial'                : self.handlerEventDial,
            'NewCallerid'         : self.handlerEventNewcallerid,
            'SessionLimit'        : self.handlerEventSessionLimit,
        }

    def handlerEventDial(self, ami, event):
        # print 'Server %s :: Processing Event Dial...' % ami
        subevent = event.get('subevent', "begin")
        if subevent.lower() == 'begin':
            destination = event['destination']
            for s in extensions.keys():
                if destination.startswith(s):
                    try:
                        user = UserPi.objects.get(Q(phone__icontains=kill_4744(event['calleridnum'])) | Q(phone2__icontains=kill_4744(event['calleridnum'])))
                        RedisPublisher(facility='call_incoming', broadcast=True).publish_message(
                            RedisMessage('%s' % json.dumps(
                                {'num': event['calleridnum'], 'uid': user.user_id_id, 'login': user.user_id.login,
                                 'uni_id': event['uniqueid'],
                                 'channel': event['channel'], 'begin': 'begin', 'cidname': event['calleridname']})))

                    except:
                        RedisPublisher(facility='call_incoming', broadcast=True).publish_message(
                            RedisMessage('%s' % json.dumps(
                                {'num': event['calleridnum'],
                                 'uni_id': event['uniqueid'],
                                 'channel': event['channel'], 'begin': 'begin', 'cidname': event['calleridname']})))

        elif subevent.lower() == 'end':
            # print 'Server %s :: Processing Event Dial -> SubEvent End...' % ami
            RedisPublisher(facility='call_incoming', broadcast=True).publish_message(RedisMessage('%s' % json.dumps(
                {'uni_id': event['uniqueid'],
                 'begin': 'end'})))

    # def handlerEventDial(self, ami, event):
    #     print event
    #     if 'destination' in event:
    #         destination = event['destination']
    #         for s in extensions.keys():
    #             if destination.startswith(s):
    #                 print event
    #                 print UserPi.objects.get(phone__icontains=event['calleridnum'])
    #                 user = UserPi.objects.get(phone__icontains=event['calleridnum'])
    #                 if user != None:
    #                     cid = event['calleridnum']
    #                     cidname = event['calleridname']
    #                     extname = extensions[s]
    #                     uni_id = event['uniqueid']
    #                     channel = event['channel']
    #                     print user
    #                     RedisPublisher(facility='call_incoming', broadcast=True).publish_message(RedisMessage('%s' % json.dumps({'num': cid, 'uid': user.user_id.id, 'login': user.user_id.login, 'extname': extname, 'uni_id': uni_id, 'channel': channel})))
    #                 else:
    #                     print 'pass'

            # calls = AsteriskCall.objects.create(uniqueid=event['uniqueid'], caller_num=event['calleridnum'],
            #                                     destination_num=event['connectedlinenum'], status='0',
            #                                     start_call=datetime.datetime.fromtimestamp(
            #                                         float(event['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'))


    def handlerEventHangup(self, ami, event):
        pass
        # print 'Hangup'
        # print event

    def handlerEventNewcallerid(self, ami, event):
        pass
        # log.debug("Server %s :: Processing Event Newcallerid..." % ami.servername)
        # uniqueid = event.get('uniqueid')
        # channel = event.get('channel')
        # calleridnum = event.get('calleridnum', event.get('callerid'))
        # calleridname = event.get('calleridname')


    def handlerEventSessionLimit(self, ami, event):
        pass

