from django.db import models

class DomainMap(models.Model):
    domain = models.CharField('DomainMap', max_length=128, db_index=True)
    project_name = models.CharField('Project name', max_length=128)

    def __unicode__(self):
        return self.domain

    class Meta:
        db_table = 'domain_map'
