from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

<<<<<<< Updated upstream:bhp077/apps/microbiome_maternal/admin/maternal_srh_admin.py
from bhp077.apps.microbiome_maternal.models import MaternalSrh
from bhp077.apps.microbiome_maternal.forms import MaternalSrhForm


class MaternalSrhAdmin(BaseModelAdmin):

    form = MaternalSrhForm
=======
from bhp077.apps.microbiome_maternal.models import Srh
from bhp077.apps.microbiome_maternal.forms import SrhForm


class SrhAdmin(BaseModelAdmin):

    form = SrhForm
>>>>>>> Stashed changes:bhp077/apps/microbiome_maternal/admin/srh_services_utilization_admin.py

    fields = ('seen_at_clinic',
              'reason_unseen_clinic',
              'reason_unseen_clinic_other',
              'is_contraceptive_initiated',
              'contraceptive_methods',
              'reason_not_initiated',
              'srh_referral',
              'srh_referral_other')
    radio_fields = {'seen_at_clinic': admin.VERTICAL,
                    'reason_unseen_clinic': admin.VERTICAL,
                    'is_contraceptive_initiated': admin.VERTICAL,
                    'reason_not_initiated': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptive_methods',)

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

<<<<<<< Updated upstream:bhp077/apps/microbiome_maternal/admin/maternal_srh_admin.py
admin.site.register(MaternalSrh, MaternalSrhAdmin)
=======
admin.site.register(Srh, SrhAdmin)
>>>>>>> Stashed changes:bhp077/apps/microbiome_maternal/admin/srh_services_utilization_admin.py
