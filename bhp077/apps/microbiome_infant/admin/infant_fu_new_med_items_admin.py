from django.contrib import admin

from ..models import InfantFuNewMedItems


class InfantFuNewMedItemsAdmin(admin.ModelAdmin):

    radio_fields = {
        'medication': admin.VERTICAL,
        'drug_route': admin.VERTICAL,
    }
admin.site.register(InfantFuNewMedItems, InfantFuNewMedItemsAdmin)
