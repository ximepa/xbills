#!/usr/bin/env python
from twisted.internet import reactor
from manager import AMIFactory
from twisted.internet import task
from xbills import settings
import logging




extensions={"SIP/72":"monitoring"}

 
log = logging.getLogger("pyCalledMe2")
 
timeouttask=None
timeoutping=5
timeoutloop=30
 
class callMeFactory(AMIFactory):
    cbconnect=None
    def __init__(self):
        AMIFactory.__init__(self, settings.VOIP_USERNAME, settings.VOIP_SECRET)
    def connect(self):
        df = self.login(settings.VOIP_IP_ADDRESS, settings.VOIP_PORT)
        if self.cbconnect!=None:
            df.addCallback(self.cbconnect)
    def clientConnectionLost(self,connector,reason):
        log.info("connection lost - connecting again")
    def clientConnectionFailed(self,connector,reason):
        log.info("connection failed - connecting again")

def onDial(protocol,event):
    print event
    if 'destination' in event:
        destination=event['destination']
        print destination
        print extensions.keys()
        for s in extensions.keys():
            if destination.startswith(s):
                cid=event['calleridnum']
                cidname=event['calleridname']
                extname=extensions[s]

def checknetlink(protocol):
     
    def ontimeout():
        log.info("timeout")
        if dc.active():
            dc.cancel()
        timeouttask.stop()
        protocol.transport.loseConnection()
         
         
    def canceltimeout(*val):
        if dc.active():
            dc.cancel()
 
        log.info("cancel timeout")
        #log.info(val)
         
    def success(val):
        log.info("ping")
        pass
     
    log.info("setting timeout")
    dc = reactor.callLater(timeoutping,ontimeout)
    df = protocol.ping()
    df.addBoth(canceltimeout)
    df.addCallback(success)
    df.addErrback(ontimeout)
     
 
def onLogin(protocol):
    df = protocol.registerEvent("Dial",onDial)
    global timeouttask
    timeouttask = task.LoopingCall(checknetlink,protocol)
    timeouttask.start(timeoutloop)
    return df
 
def main():
    cm = callMeFactory()
    cm.cbconnect=onLogin
    cm.connect()

def killapp(*args):
    reactor.stop()
    return True
