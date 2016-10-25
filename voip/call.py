import json
from twisted.internet import reactor
import datetime
from django.conf import settings
from django.http import HttpResponse
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from manager import AMIFactory, AMIProtocol
from twisted.internet import task, defer
import logging
from voip.models import AsteriskCall
from error import AMICommandFailure
from twisted.internet import error as tw_error
from voip_events import VoipEvents

extensions={"SIP/72":"monitoring"}


timeouttask=None
timeoutping=5
timeoutloop=30



class callMeFactory(AMIFactory):
    cbconnect=None
    def __init__(self):
        AMIFactory.__init__(self, settings.VOIP_USER, settings.VOIP_PASSWORD)
    def connect(self):
        df = self.login(settings.VOIP_IP_ADDRESS, settings.VOIP_PORT)
        df.addCallback(self.cbconnect)
    def clientConnectionLost(self,connector,reason):
        reactor.callLater(1, self.connect)
        print 'connection lost - connecting again'
    def clientConnectionFailed(self,connector,reason):
        reactor.callLater(1, self.connect)
        print 'connection failed - connecting again'

def onLogin(protocol):
    global session
    session= protocol
    eventHandlers = VoipEvents().eventHandlers
    for event, handler in eventHandlers.items():
        print "Server :: Registering EventHandler for %s" % event
        protocol.registerEvent(event, handler)


    # df = protocol.registerEvent("Dial",onDial)
    # global timeouttask
    # timeouttask = task.LoopingCall(checknetlink,protocol)
    # timeouttask.start(timeoutloop)
    # return df


def call_run():
    cm = callMeFactory()
    cm.cbconnect=onLogin
    cm.connect()

def hangup(request):
    print request.GET
    if 'channel' in request.GET:
        session.hangup(channel=request.GET['channel'])
    # session.redirect(channel='', exten='SIP/72', context='default', priority=1)




