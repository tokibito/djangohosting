#!/usr/bin/env python
from wsgiref.simple_server import make_server, WSGIServer
from SocketServer import ThreadingMixIn

from django.utils.daemonize import become_daemon

from wsgi import WSGIHandler

class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    pass

def runserver(host, port):
    httpd = make_server(host, port, WSGIHandler(), ThreadingWSGIServer)
    httpd.serve_forever()

if __name__ == '__main__':
    import sys
    from conf import Settings
    settings = Settings()
    if settings.server.daemonize:
        become_daemon()
    if len(sys.argv) == 2:
        runserver(sys.argv[1], 8000)
    elif len(sys.argv) >= 3:
        runserver(sys.argv[1], sys.argv[2])
    else:
        runserver(settings.server.host, settings.server.port)
