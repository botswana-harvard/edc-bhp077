from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

from ..models import SexualReproductiveHealth
from ..forms import SexualReproductiveHealthForm


class SexualReproductiveHealthAdmin(BaseModelAdmin):

    form = SexualReproductiveHealthForm

    fields = ('more_children',
              'next_child',
              'contraceptive_measure',
              'uses_contraceptive',
              'contraceptives_used',
              'contraceptives_used_other',
              'srh_referral')
    radio_fields = {'more_children': admin.VERTICAL,
                    'next_child': admin.VERTICAL,
                    'contraceptive_measure': admin.VERTICAL,
                    'uses_contraceptive': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptives_used',)

    actions = [
        export_as_csv_action(
            description="CSV Export of Sexual Reproductive Health",
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

admin.site.register(SexualReproductiveHealth, SexualReproductiveHealthAdmin)
