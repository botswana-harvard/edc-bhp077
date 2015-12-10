from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

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
        "death_cause_category_other",
        "dx_code",
        "dx_code_other",
        "illness_duration",
        "death_medical_responsibility",
        "participant_hospitalized",
        "death_reason_hospitalized",
        "death_reason_hospitalized_other",
        "days_hospitalized",
        "comment")
    radio_fields = {
        "death_cause_info": admin.VERTICAL,
        "perform_autopsy": admin.VERTICAL,
        "participant_hospitalized": admin.VERTICAL,
        "death_cause_category": admin.VERTICAL,
        "death_cause_category": admin.VERTICAL,
        "dx_code": admin.VERTICAL,
        "death_medical_responsibility": admin.VERTICAL,
        "death_reason_hospitalized": admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Death",
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
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalDeathAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalDeath, MaternalDeathAdmin)
