from django.contrib import admin

from ..models import InfantFu


class InfantFuAdmin(admin.ModelAdmin):

    list_display = (
        'physical_assessment',
        'diarrhea_illness',
        'has_dx',
        'was_hospitalized',
        'days_hospitalized',
    )

    radio_fields = {
        'physical_assessment': admin.VERTICAL,
        'diarrhea_illness': admin.VERTICAL,
        'has_dx': admin.VERTICAL,
        'was_hospitalized': admin.VERTICAL,
    }

admin.site.register(InfantFu, InfantFuAdmin)
