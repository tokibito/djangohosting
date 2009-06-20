import sys
from optparse import make_option

from django.core.management.base import BaseCommand

from ddns_update.models import DDNSProfile

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--ieserver', action='store_true',
                dest='ieserver', help='update DDNS service by ieserver'),
    )
    args = '[optional]'

    def _update(self, profile):
        sys.stdout.write('updating %s.%s ... ' % (profile.account, profile.domain))
        if profile.update():
            sys.stdout.write('ok\n')
        else:
            sys.stdout.write('error\n')

    def handle(self, *args, **options):
        if options['ieserver']:
            sys.stdout.write('update ieserver domain...\n')
            for profile in DDNSProfile.objects.ieservers():
                self._update(profile)
            return

        sys.stdout.write('update all domain...\n')
        for profile in DDNSProfile.objects.all():
            self._update(profile)
