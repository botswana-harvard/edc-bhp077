from django.contrib import admin
from edc.subject.off_study.admin import BaseOffStudyModelAdmin

from ..models import InfantOffStudy
from ..forms import InfantOffStudyForm


class InfantOffStudyAdmin(BaseOffStudyModelAdmin):

    form = InfantOffStudyForm
    dashboard_type = 'infant'
    visit_model_name = 'infantvisit'

    fields = (
        'registered_subject',
        'infant_visit',
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

admin.site.register(InfantOffStudy, InfantOffStudyAdmin)
