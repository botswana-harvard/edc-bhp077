from django.contrib import admin

from edc.subject.appointment.admin import BaseAppointmentModelAdmin

from ..forms import MaternalVisitForm
from ..models import MaternalVisit
from bhp077.apps.microbiome_lab.models import MaternalRequisition


class MaternalVisitAdmin(BaseAppointmentModelAdmin):

    form = MaternalVisitForm

    visit_model_instance_field = 'maternal_visit'

    requisition_model = MaternalRequisition

    dashboard_type = 'maternal'

admin.site.register(MaternalVisit, MaternalVisitAdmin)
