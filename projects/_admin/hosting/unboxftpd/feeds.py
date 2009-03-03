from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.feeds import Feed

from models import FTPLog

class FTPLogFeed(Feed):
    title = _('FTPD log')
    description = _('FTPD log feeds.')
    log_model = FTPLog
    mode = None
    num_output = 100

    def items(self):
        logs = self.log_class.objects.all()
        if self.mode:
            logs = logs.filter(mode=self.mode)
        return logs[:self.num_output]

    def item_pubdate(self, item):
        return item.create_at
