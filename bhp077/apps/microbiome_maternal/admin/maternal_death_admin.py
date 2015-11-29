from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.subject.registration.models import RegisteredSubject

from .registered_subject_model_admin import RegisteredSubjectModelAdmin
from bhp077.apps.microbiome_maternal.forms import MaternalDeathForm
from bhp077.apps.microbiome_maternal.models import MaternalDeath, MaternalVisit


class MaternalDeathAdmin(BaseModelAdmin):

    form = MaternalDeathForm
    fields = (
        "maternal_visit",
        "death_date",
        "death_cause_info",
        "death_cause_info_other",
        "perform_autopsy",
        "death_cause",
        "death_cause_category",
        "death_cause_other",
        "dx_code",
        "illness_duration",
        "death_medical_responsibility",
        "participant_hospitalized",
        "death_reason_hospitalized",
        "days_hospitalized",
        "comment")
    radio_fields = {
        "perform_autopsy": admin.VERTICAL,
        "participant_hospitalized": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalDeathAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalDeath, MaternalDeathAdmin)
