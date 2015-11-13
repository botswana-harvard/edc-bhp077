from django.contrib import admin

from ..models import InfantFuNewMedItems

from edc.base.modeladmin.admin import BaseModelAdmin


class InfantFuNewMedItemsAdmin(BaseModelAdmin):

    radio_fields = {
        'medication': admin.VERTICAL,
        'drug_route': admin.VERTICAL,
    }
admin.site.register(InfantFuNewMedItems, InfantFuNewMedItemsAdmin)
