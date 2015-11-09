from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import InfantBirthDataForm
from ..models import InfantBirthData, InfantVisit, InfantBirth


class InfantBirthDataAdmin(BaseModelAdmin):

    form = InfantBirthDataForm

    fields = (
        "infant_visit",
        "infant_birth",
        "infant_birth_weight",
        "infant_length",
        "head_circumference",
        "apgar_score",
        "apgar_score_min_1",
        "apgar_score_min_5",
        "apgar_score_min_10",
        "congenital_anomalities",
        "other_birth_info")

    radio_fields = {
        "apgar_score": admin.VERTICAL,
        "congenital_anomalities": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_birth":
            if request.GET.get('infant_visit'):
                infant_visit = InfantVisit.objects.get(id=request.GET.get('infant_visit'))
                kwargs["queryset"] = InfantBirth.objects.filter(registered_subject=infant_visit.appointment.registered_subject)
        return super(InfantBirthDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantBirthData, InfantBirthDataAdmin)
