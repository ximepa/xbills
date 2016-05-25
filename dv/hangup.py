import pyrad
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from core.models import Nas


def Hangup(server, session):
    ip = Nas.objects.get(id=server).ip
    sclient = Client(server=ip, secret="radsecret", acctport=3799, dict=Dictionary("dictionary"))
    req = sclient.CreateAcctPacket(code=pyrad.packet.DisconnectRequest)
    req["Acct-Session-Id"] = session
    reply = sclient.SendPacket(req)
    return reply