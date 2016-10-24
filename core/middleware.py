from django.core.cache import cache
from django.conf import settings
from core.models import Admin
import json
import datetime
from threading import Thread
import time
import psutil
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from core.commands import strfdelta


ONLINE_THRESHOLD = getattr(settings, 'ONLINE_THRESHOLD', 60 * 0.5)
ONLINE_MAX = getattr(settings, 'ONLINE_MAX', 50)

def get_online_now(self):
    admin = Admin.objects.filter(id__in=self.online_now_ids or [])
    l = []
    for a in admin:
        l.append(a.login)
    print l
    return l


class OnlineNowMiddleware(object):
    """
    Maintains a list of users who have interacted with the website recently.
    Their user IDs are available as ``online_now_ids`` on the request object,
    and their corresponding users are available (lazily) as the
    ``online_now`` property on the request object.
    """

    def process_request(self, request):
        # First get the index
        uids = cache.get('online-now', [])

        # Perform the multiget on the individual online uid keys
        online_keys = ['online-%s' % (u,) for u in uids]
        fresh = cache.get_many(online_keys).keys()
        online_now_ids = [int(k.replace('online-', '')) for k in fresh]

        # If the user is authenticated, add their id to the list
        if request.user.is_authenticated():
            uid = request.user.id
            # If their uid is already in the list, we want to bump it
            # to the top, so we remove the earlier entry.
            if uid in online_now_ids:
                online_now_ids.remove(uid)
            online_now_ids.append(uid)
            if len(online_now_ids) > ONLINE_MAX:
                del online_now_ids[0]

        # Attach our modifications to the request object
        request.__class__.online_now_ids = online_now_ids
        request.__class__.online_now = property(get_online_now)

        # Set the new cache
        cache.set('online-%s' % (request.user.pk,), True, ONLINE_THRESHOLD)
        cache.set('online-now', online_now_ids, ONLINE_THRESHOLD)


class ThreadingDashboardMiddleware(object):

    def __init__(self, interval=10):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        psutil.boot_time()
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        while True:
            time.sleep(7)
            # Do something
            try:
                list = []
                data_dict = {}
                d2 = datetime.datetime.now()
                diff = abs((d2 - boot_time))
                for getCpu in psutil.cpu_percent(interval=1, percpu=True):
                    pinfo = {}
                    pinfo['core'] = getCpu
                    list.append(pinfo)
                data_dict.update({
                    "cpu": list,
                    "memory": [{
                        "cur": psutil.virtual_memory().percent,
                        "total": psutil.virtual_memory().total,
                        "used": psutil.virtual_memory().used,
                        "free": psutil.virtual_memory().free,
                        "cached": psutil.virtual_memory().cached,
                        "swap": psutil.swap_memory().percent,
                        "stotal": psutil.swap_memory().total,
                        "sused": psutil.swap_memory().used,
                        "sfree": psutil.swap_memory().free,
                    }],
                    "uptime": strfdelta(diff, settings.UPTIME_FORMAT)
                })
                get_pc_info = json.dumps(data_dict)
                RedisPublisher(facility='dashboard', broadcast=True).publish_message(RedisMessage('%s' % get_pc_info))
                #time.sleep(1)
            except:
                pass






