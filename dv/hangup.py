import pyrad
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from core.models import Nas


def Hangup(server, session):
    nas = Nas.objects.get(id=server)
    client = Client(server=nas.ip, secret="radsecret", acctport=3799, dict=Dictionary("dictionary"))
    req = client.CreateAcctPacket(code=pyrad.packet.DisconnectRequest)
    req["Acct-Session-Id"] = session
    reply = client.SendPacket(req)
    return reply