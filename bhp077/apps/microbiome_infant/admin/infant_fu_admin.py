from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import InfantFuForm
from ..models import InfantVisit, InfantFu


class InfantFuAdmin(BaseModelAdmin):
    form = InfantFuForm

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantFuAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFu, InfantFuAdmin)
