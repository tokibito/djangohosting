import os
import sys

from django.conf import settings

try:
    from pyftpdlib.ftpserver import FTPHandler
except ImportError:
    from unboxftpd.pyftpdlib.ftpserver import FTPHandler

from unboxftpd.models import FTPUser, FTPLog

class Authorizer(object):
    """
    Authorizer class by FTPUser model.
    """
    user_class = FTPUser

    def get_user(self, username):
        return self.user_class.get_user(username)

    def validate_authentication(self, username, password):
        user = self.get_user(username)
        return user and user.check_password(password)

    def impersonate_user(self, username, password):
        pass    

    def terminate_impersonation(self):
        pass

    def has_user(self, username):
        return self.get_user(username)

    def get_home_dir(self, username):
        user = self.get_user(username)
        # return ascii
        return user and str(user.home_directory)

    def get_msg_login(self, username):
        user = self.get_user(username)
        if user:
            user.login_update()
        return 'welcome.'

    def get_msg_quit(self, username):
        return 'good bye.'

    def has_perm(self, username, perm, path=None):
        user = self.get_user(username)
        return user and user.has_perm(perm, path)

    def get_perms(self, username):
        user = self.get_ftpuser(username)
        return user and user.get_perms()

class LoggingHandler(object):
    log_class = FTPLog
    user_class = FTPUser

    def __call__(self, ftp_handler, line, mode):
        """
        logging handler
        """
        user = self.user_class.get_user(ftp_handler.username)

        # TODO detect or force convert
        #if ftp_handler.is_client_utf8:
        #    line = unicode(line, 'utf-8')

        if user:
            self.log_class.logging(
                user=user,
                mode=mode,
                filename=os.path.basename(line),
                remote_path=ftp_handler.fs.ftpnorm(line),
                local_path=ftp_handler.fs.ftp2fs(line)
            )

class LoggingFTPHandler(FTPHandler):
    """
    FTPHandler with simple logging.
    """
    logging_handler = LoggingHandler()
    is_client_utf8 = False

    def __init__(self, *args, **kwargs):
        FTPHandler.__init__(self, *args, **kwargs)
        if self.get_encoding() == 'UTF-8':
            self._extra_feats += ['UTF8']

    def ftp_STOR(self, line, mode='w'):
        """
        upload
        """
        FTPHandler.ftp_STOR(self, line, mode=mode)
        self.logging(line, 'STOR')

    def ftp_RETR(self, line):
        """
        download
        """
        FTPHandler.ftp_RETR(self, line)
        self.logging(line, 'RETR')

    def ftp_DELE(self, line):
        """
        delete
        """
        FTPHandler.ftp_DELE(self, line)
        self.logging(line, 'DELE')

    def ftp_OPTS(self, line):
        """
        opts for utf8 encoding.
        """
        if line.count(' ') == 1:
            cmd, arg = line.upper().split(' ')
            if cmd == 'UTF8' and arg == 'ON' and  \
                    self.get_encoding() == 'UTF-8':
                self.is_client_utf8 = True
                self.respond('200 OK.')
                return
        FTPHandler.ftp_OPTS(self, line)

    def get_encoding(self):
        return sys.getfilesystemencoding().upper()

    def logging(self, line, mode):
        if self.logging_handler:
            try:
                self.logging_handler(ftp_handler=self, line=line, mode=mode)
            except:
                if settings.DEBUG:
                    raise
