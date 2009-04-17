import sys
import os
from StringIO import StringIO
from multiprocessing import Process, Pipe

from conf import Settings
import utils as host_utils

def handle_exception(status, start_response, msg=None):
    try:
        start_response(status, [('Content-Type', 'text/plain')])
    except:
        pass
    return msg or status

def handle_project(host_settings, username, project_name, environ, proj_conn):
    # set django settings environ
    os.environ['DJANGO_SETTINGS_MODULE'] = project_name + '.settings'

    # append project directory to sys.path
    django_proj_dir_parent = os.path.join(os.path.abspath(host_settings.hosting.project_dir), username)
    django_proj_dir = os.path.join(django_proj_dir_parent, project_name)
    if not django_proj_dir_parent in sys.path:
        sys.path.append(django_proj_dir_parent)
    if not django_proj_dir in sys.path:
        sys.path.append(django_proj_dir)

    try:
        from django.conf import settings
        from django.core.handlers.wsgi import WSGIHandler as DjangoHandler
 
        # create django handler
        application = DjangoHandler()
 
        # admin media
        if host_settings.hosting.admin_media:
            from django.core.servers.basehttp import AdminMediaHandler
            application = AdminMediaHandler(application)
 
        def start_response(status, headers, exec_info=None):
            # send start_response args
            proj_conn.send([status, headers])
 
        # handle application
        resp = application(environ, start_response)
    except:
        resp = handle_exception('500 Internal Server error',
                start_response, msg='application handle error.')

    # send response
    proj_conn.send(resp)
    proj_conn.close()

class WSGIHandler(object):

    def __init__(self, settings=None):
        self.settings = settings or Settings()

    def __call__(self, environ, start_response):
        domain, port = host_utils.split_hostname(environ['HTTP_HOST'])

        if not domain.endswith(self.settings.hosting.domain):
            return handle_exception('404 Not Found', start_response)
    
        name = host_utils.split_subdomain(self.settings.hosting.domain, domain)
        if not name:
            username = '_admin'
            project_name = 'hosting'
        elif name.count(host_utils.SEP_DOMAIN) == 1:
            project_name, username = host_utils.split_domain(name)
        else:
            return handle_exception('403 Forbidden', start_response)

        app_dir = os.path.join(os.path.abspath(self.settings.hosting.project_dir), '%s.%s' % (project_name, username))
        app_settings = os.path.join(app_dir, 'settings.py')
        if not os.path.exists(app_settings):
            return handle_exception('404 Not Found', start_response)

        handler_conn, proj_conn = Pipe()
        proc = Process(target=handle_project, args=(self.settings, username, project_name, environ, proj_conn))
        proc.start()
        start_response(*handler_conn.recv())
        resp = handler_conn.recv()
        proc.join()
        return resp
