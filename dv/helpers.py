import pyrad
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from core.models import Server


def Hangup(server, port, session, user_name):
    server = Server.objects.get(id=server)
    print server.get_hash_password
    client = Client(server=server.ip, secret=server.get_hash_password, acctport=3799, dict=Dictionary("dictionary"))
    if 'mx80' in server.server_type:
        req = client.CreateAcctPacket(code=pyrad.packet.DisconnectRequest)
        req["Acct-Session-Id"] = session
        reply = client.SendPacket(req)
        return reply
    if 'mpd5' in server.server_type:
        req = client.CreateAcctPacket(code=pyrad.packet.DisconnectRequest)
        req["User-Name"] = user_name
        reply = client.SendPacket(req)
        return reply