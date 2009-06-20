import re
import socket
from urllib import urlencode
from urllib2 import urlopen

# socket timeout second
socket.setdefaulttimeout(60)

RE_IP_ADDRESS = re.compile('^\d+\.\d+\.\d+\.\d+$')

URL_GET_REMOTE_ADDR = 'http://ipcheck.ieserver.net/'
URL_DDNS_UPDATE = 'https://ieserver.net/cgi-bin/dip.cgi'

def get_remote_addr():
    try:
        conn = urlopen(URL_GET_REMOTE_ADDR)
        ip = conn.read()
        conn.close()
        if RE_IP_ADDRESS.match(ip):
            return ip
    except:
        pass

def update(username, password, domain):
    # parse url parameter
    params = urlencode({
        'username': username,
        'password': password,
        'domain': domain,
        'updatehost': 1,
    })

    try:
        conn = urlopen('%s?%s' % (URL_DDNS_UPDATE, params))
        page = conn.read()
        conn.close()
        return page
    except:
        pass

def validate_updated(page, ip):
    re_ip = re.compile('%s' % ip.replace('.', r'\.'))
    return not not re_ip.search(page)
