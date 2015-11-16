from django.contrib import admin

from ..models import InfantFuPhysical

from edc.base.modeladmin.admin import BaseModelAdmin


class InfantFuPhysicalAdmin(BaseModelAdmin):

    list_display = ('has_abnormalities', )

    radio_fields = {'has_abnormalities': admin.VERTICAL, }

admin.site.register(InfantFuPhysical, InfantFuPhysicalAdmin)
