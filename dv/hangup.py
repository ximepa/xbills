import pyrad
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from core.models import Nas


def Hangup(server, session):
    ip = Nas.objects.get(id=server).ip
    print ip
    sclient = Client(server=ip, secret="radsecret", acctport=3799, dict=Dictionary("dictionary"))
    print sclient
    req = sclient.CreateAcctPacket(code=pyrad.packet.DisconnectRequest)
    print req

    print "Sending accounting stop packet"
    req["Acct-Session-Id"] = session
    print req
    reply = sclient.SendPacket(req)