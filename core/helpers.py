import random
from django.conf import settings
import os
import pexpect
import subprocess



def randomDigits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)


def module_check(module):
    modules = settings.INSTALLED_APPS
    module_path = os.path.join(settings.BASE_DIR,  module)
    if module in modules and os.path.exists(module_path):
        return True
    else:
        return False


def test_mac(host, user, passwd, mac):
    child = pexpect.spawn('telnet %s' % host)
    child.expect('login : ')
    child.sendline('%s' % user)
    child.expect('password : ')
    child.sendline('%s' % passwd)
    child.expect('->')
    child.sendline('show mac-address-table %s' % mac)
    child.expect('->')
    responce_mac = child.before
    child.sendline('show arp %s' % mac)
    child.expect('->')
    responce_arp = child.before
    child.sendline('exit')
    child.expect(pexpect.EOF)
    splited_responce_mac = responce_mac.split()
    vlan = splited_responce_mac[20]
    if vlan != 'VLAN':
        return None
    else:
        try:
            splited_responce_arp = responce_arp.split()
            #splited_responce_arp[21]
            ping = subprocess.Popen(
                ["ping", "-c", "5", '-i', '0.2', "-l", "1", "-s", "1400", "-W", "1", splited_responce_arp[21]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, error = ping.communicate()
            splited_out = out.splitlines()
            data = {
                  'vlan': splited_responce_mac[21],
                  'mac': splited_responce_mac[22],
                  'port': splited_responce_mac[26],
                  'ip': splited_responce_arp[21],
                  'ping': splited_out[8]
            }
        except:
            data = {
                  'vlan': splited_responce_mac[21],
                  'mac': splited_responce_mac[22],
                  'port': splited_responce_mac[26],
                  'ip': 'Not found',
                  'ping': 'Not responsive'
            }
    return data