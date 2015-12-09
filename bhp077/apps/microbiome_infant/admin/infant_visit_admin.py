from django.contrib import admin

from edc.subject.appointment.admin import BaseAppointmentModelAdmin

from bhp077.apps.microbiome_lab.models import InfantRequisition

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

admin.site.register(InfantVisit, InfantVisitAdmin)
