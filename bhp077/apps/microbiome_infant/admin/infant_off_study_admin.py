from collections import OrderedDict

from django.contrib import admin

from edc.subject.off_study.admin import BaseOffStudyModelAdmin
from edc.export.actions import export_as_csv_action

from ..models import InfantOffStudy
from ..forms import InfantOffStudyForm


class InfantOffStudyAdmin(BaseOffStudyModelAdmin):

    form = InfantOffStudyForm
    dashboard_type = 'infant'
    visit_model_name = 'infantvisit'

    fields = (
        'registered_subject',
        'infant_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'reason_other',
        'has_scheduled_data',
        'comment',
    )

    list_display = (
        'infant_visit',
        'offstudy_date',
        'reason',
        'has_scheduled_data',)

    radio_fields = {'has_scheduled_data': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Off Study",
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

admin.site.register(InfantOffStudy, InfantOffStudyAdmin)
