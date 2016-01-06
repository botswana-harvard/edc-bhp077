from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_export.actions import export_as_csv_action

from microbiome.apps.mb.constants import INFANT

from ..forms import InfantOffStudyForm
from ..models import InfantOffStudy


class InfantOffStudyAdmin(BaseModelAdmin):

    form = InfantOffStudyForm
    dashboard_type = INFANT
    visit_model_name = 'infantvisit'

    fields = (
        'registered_subject',
        'infant_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'reason_other',
        'comment',
    )

    list_display = (
        'infant_visit',
        'offstudy_date',
        'reason')

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
