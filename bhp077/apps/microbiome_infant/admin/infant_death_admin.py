from collections import OrderedDict

from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import InfantDeathForm
from ..models import InfantDeath, InfantVisit

from edc.export.actions import export_as_csv_action


class InfantDeathAdmin(BaseModelAdmin):

    form = InfantDeathForm

    fields = (
        "infant_visit",
        "death_date",
        "death_cause_info",
        "death_cause_info_other",
        "perform_autopsy",
        "death_cause",
        "death_cause_category",
        "death_cause_category_other",
        "dx_code",
        "dx_code_other",
        "illness_duration",
        "death_medical_responsibility",
        "participant_hospitalized",
        "death_reason_hospitalized",
        "death_reason_hospitalized_other",
        "days_hospitalized",
        "study_drug_relate",
        "infant_nvp_relate",
        "haart_relate",
        "trad_med_relate",
        "comment",
    )

    radio_fields = {
        "death_reason_hospitalized": admin.VERTICAL,
        "death_medical_responsibility": admin.VERTICAL,
        "death_cause_info": admin.VERTICAL,
        "death_cause_category": admin.VERTICAL,
        "perform_autopsy": admin.VERTICAL,
        "participant_hospitalized": admin.VERTICAL,
        "study_drug_relate": admin.VERTICAL,
        "infant_nvp_relate": admin.VERTICAL,
        "haart_relate": admin.VERTICAL,
        "trad_med_relate": admin.VERTICAL,
        "dx_code": admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Death",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
            if request.GET.get('infant_visit'):
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantDeathAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantDeath, InfantDeathAdmin)
