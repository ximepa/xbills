from threading import Thread
from twisted.internet import reactor

from voip.call import call_run


class ThreadingCallsMiddleware(object):

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        #self.interval = interval
        reactor.callWhenRunning(call_run)
        Thread(target=reactor.run, name='call', args=(False,)).start()
