import pyrad
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from core.models import Nas


def Hangup(server, port, session, user_name):
    nas = Nas.objects.get(id=server)
    print nas.get_hash_password
    client = Client(server=nas.ip, secret=nas.get_hash_password, acctport=3799, dict=Dictionary("dictionary"))
    if 'mx80' in nas.nas_type:
        req = client.CreateAcctPacket(code=pyrad.packet.DisconnectRequest)
        req["Acct-Session-Id"] = session
        reply = client.SendPacket(req)
        return reply
    if 'mpd5' in nas.nas_type:
        req = client.CreateAcctPacket(code=pyrad.packet.DisconnectRequest)
        req["User-Name"] = user_name
        reply = client.SendPacket(req)
        return reply