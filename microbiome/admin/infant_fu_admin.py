from django.contrib import admin

from ..models import InfantFu, InfantFuPhysical

from .site import admin_site


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

admin_site.register(InfantFu, InfantFuAdmin)


class InfantFuPhysicalAdmin(admin.ModelAdmin):

    list_display = (
        'has_abnormalities',
    )

admin_site.register(InfantFuPhysical, InfantFuPhysicalAdmin)
