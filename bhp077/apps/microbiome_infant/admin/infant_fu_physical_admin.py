from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import InfantFuPhysicalForm
from ..models import InfantVisit, InfantFuPhysical


class InfantFuPhysicalAdmin(BaseModelAdmin):
    form = InfantFuPhysicalForm

    radio_fields = {
        'general_activity': admin.VERTICAL,
        'physical_exam_result': admin.VERTICAL,
        'heent_exam': admin.VERTICAL,
        'resp_exam': admin.VERTICAL,
        'cardiac_exam': admin.VERTICAL,
        'abdominal_exam': admin.VERTICAL,
        'skin_exam': admin.VERTICAL,
        'macular_papular_rash': admin.VERTICAL,
        'neurologic_exam': admin.VERTICAL
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantFuPhysicalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFuPhysical, InfantFuPhysicalAdmin)
