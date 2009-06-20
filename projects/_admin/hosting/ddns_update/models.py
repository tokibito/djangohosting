from django.db import models

from ddns_update.ddns import ieserver

class ServiceNotSupported(Exception):
    pass

DDNS_ID_IESERVER = 1
DDNS_SERVICES = (
    (DDNS_ID_IESERVER, 'ieserver'),
)

class DDNSProfileManager(models.Manager):
    def ieservers(self):
        return self.filter(service=DDNS_ID_IESERVER)

class DDNSProfile(models.Model):
    domain = models.CharField('Domain', max_length=64)
    service = models.IntegerField('Service', choices=DDNS_SERVICES, db_index=True)
    account = models.CharField('Account', max_length=128)
    password = models.CharField('Password', max_length=64)

    objects = DDNSProfileManager()

    def update(self):
        if self.service == DDNS_ID_IESERVER:
            return ieserver.update(self.account, self.password, self.domain)
        raise ServiceNotSupported

    class Meta:
        db_table = 'ddns_profile'
        verbose_name = 'DDNS Profile'
        verbose_name_plural = 'DDNS Profile'
