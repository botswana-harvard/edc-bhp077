from django.contrib import admin

from ..models import InfantFuPhysical

from .site import admin_site


class InfantFuPhysicalAdmin(admin.ModelAdmin):

    list_display = ('has_abnormalities', )

    radio_fields = {'has_abnormalities': admin.VERTICAL, }

admin_site.register(InfantFuPhysical, InfantFuPhysicalAdmin)
