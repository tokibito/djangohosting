from django.contrib import admin
from ddns_update.models import DDNSProfile

class DDNSProfileAdmin(admin.ModelAdmin):
    list_display = ('account', 'domain', 'service')

    class Meta:
        model = DDNSProfile

admin.site.register(DDNSProfile, DDNSProfileAdmin)
