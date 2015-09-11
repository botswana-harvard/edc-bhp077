from django.contrib import admin

from ..models import InfantFuNewMedItems

from .site import admin_site


class InfantFuNewMedItemsAdmin(admin.ModelAdmin):

    radio_fields = {
        'medication': admin.VERTICAL,
        'drug_route': admin.VERTICAL,
    }
admin_site.register(InfantFuNewMedItems, InfantFuNewMedItemsAdmin)
