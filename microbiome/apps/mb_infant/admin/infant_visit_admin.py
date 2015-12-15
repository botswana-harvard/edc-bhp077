from collections import OrderedDict

from django.contrib import admin

from edc.subject.appointment.admin import BaseAppointmentModelAdmin
from edc.export.actions import export_as_csv_action

from microbiome.apps.mb_lab.models import InfantRequisition

from ..forms import InfantVisitForm
from ..models import InfantVisit


class InfantVisitAdmin(BaseAppointmentModelAdmin):

    form = InfantVisitForm

    dashboard_type = 'infant'

    requisition_model = InfantRequisition

    list_display = ('information_provider', 'information_provider_other', 'study_status', 'is_present')

    radio_fields = {
        'information_provider': admin.VERTICAL,
        'study_status': admin.VERTICAL,
        'survival_status': admin.VERTICAL,
        'is_present': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Visit",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'appointment__registered_subject__subject_identifier',
                 'gender': 'appointment__registered_subject__gender',
                 'dob': 'appointment__registered_subject__dob',
                 }),
        )]

admin.site.register(InfantVisit, InfantVisitAdmin)
