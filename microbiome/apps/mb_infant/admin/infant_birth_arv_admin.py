from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..models import InfantBirthArv

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantBirthArvAdmin(BaseInfantScheduleModelAdmin):

    list_display = ('infant_birth', 'azt_dose_date',)

    list_filter = ('azt_after_birth', 'azt_dose_date', 'azt_additional_dose', 'sdnvp_after_birth',)

    radio_fields = {
        'azt_after_birth': admin.VERTICAL,
        'azt_additional_dose': admin.VERTICAL,
        'sdnvp_after_birth': admin.VERTICAL,
        #'additional_nvp_doses': admin.VERTICAL,
        'azt_discharge_supply': admin.VERTICAL,
        #'nvp_discharge_supply': admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth Record: ARV",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_visit__appointment__registered_subject__dob',
                 }),
        )]

admin.site.register(InfantBirthArv, InfantBirthArvAdmin)
