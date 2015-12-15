from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

from ..forms import MaternalSrhForm
from ..models import MaternalSrh


class MaternalSrhAdmin(BaseModelAdmin):

    form = MaternalSrhForm

    fields = ('seen_at_clinic',
              'reason_unseen_clinic',
              'reason_unseen_clinic_other',
              'is_contraceptive_initiated',
              'contraceptives',
              'reason_not_initiated',
              'srh_referral',
              'srh_referral_other')
    radio_fields = {'seen_at_clinic': admin.VERTICAL,
                    'reason_unseen_clinic': admin.VERTICAL,
                    'is_contraceptive_initiated': admin.VERTICAL,
                    'reason_not_initiated': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptives',)

    actions = [
        export_as_csv_action(
            description="CSV Export of SRH Services Utilization",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 'registered': 'maternal_visit__appointment__registered_subject__registration_datetime'}),
        )]

admin.site.register(MaternalSrh, MaternalSrhAdmin)
