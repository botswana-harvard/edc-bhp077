from django.contrib import admin

from ..models import InfantFuNewMed

from edc.base.modeladmin.admin import BaseModelAdmin

from .infant_fu_new_med_items_admin import InfantFuNewMedItemsAdmin


class InfantFuNewMedAdmin(BaseModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }

    inlines = [InfantFuNewMedItemsAdmin, ]

admin.site.register(InfantFuNewMed, InfantFuNewMedAdmin)
