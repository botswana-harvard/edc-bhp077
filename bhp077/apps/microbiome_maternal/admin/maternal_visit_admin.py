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

    fields = (
        "appointment",
        "report_datetime",
        "info_source",
        "info_source_other",
        "reason",
        "reason_unscheduled",
        "reason_missed",
        "comments")
    
    radio_fields = {
        "reason_unscheduled": admin.VERTICAL}

    list_display = (
        'appointment',
        'report_datetime',
        'reason',
        "info_source",
        'created',
        'user_created')

    list_filter = (
        'report_datetime',
        'reason',
        'appointment__appt_status',
        'appointment__visit_definition__code')

admin.site.register(MaternalVisit, MaternalVisitAdmin)
