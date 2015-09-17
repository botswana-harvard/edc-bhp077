from django.contrib import admin

from ..models import InfantFuPhysical


class InfantFuPhysicalAdmin(admin.ModelAdmin):

    list_display = ('has_abnormalities', )

    radio_fields = {'has_abnormalities': admin.VERTICAL, }

admin.site.register(InfantFuPhysical, InfantFuPhysicalAdmin)
