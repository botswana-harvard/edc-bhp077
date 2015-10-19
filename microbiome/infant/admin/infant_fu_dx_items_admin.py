from django.contrib import admin

from ..models import InfantFuDxItems


class InfantFuDxItemsAdmin(admin.ModelAdmin):

    list_display = (
        'fu_dx',
        'health_facility',
        'was_hospitalized',
    )

    radio_fields = {
        'fu_dx': admin.VERTICAL,
        'health_facility': admin.VERTICAL,
        'was_hospitalized': admin.VERTICAL,
    }
admin.site.register(InfantFuDxItems, InfantFuDxItemsAdmin)
