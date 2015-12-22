from collections import OrderedDict

from django.contrib import admin

from edc_appointment.admin import BaseAppointmentModelAdmin
from edc_appointment.models import Appointment
from edc.export.actions import export_as_csv_action

from microbiome.apps.mb_lab.models import MaternalRequisition

from ..forms import MaternalVisitForm
from ..models import MaternalVisit


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
        "reason_missed",
        "comments")

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

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Visit",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "appointment":
                kwargs["queryset"] = Appointment.objects.filter(id=request.GET.get('appointment'))
        return super(MaternalVisitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalVisit, MaternalVisitAdmin)
