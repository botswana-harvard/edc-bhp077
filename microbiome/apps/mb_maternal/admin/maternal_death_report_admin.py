from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action
from edc.subject.registration.models import RegisteredSubject

from ..forms import MaternalDeathReportForm
from ..models import MaternalDeathReport, MaternalVisit


class MaternalDeathReportAdmin(BaseModelAdmin):

    form = MaternalDeathReportForm
    fields = (
        "maternal_visit",
        "registered_subject",
        "report_datetime",
        "death_date",
        "cause",
        "cause_other",
        "perform_autopsy",
        "death_cause",
        "cause_category",
        "cause_category_other",
        "diagnosis_code",
        "diagnosis_code_other",
        "illness_duration",
        "medical_responsibility",
        "participant_hospitalized",
        "reason_hospitalized",
        "reason_hospitalized_other",
        "days_hospitalized",
        "comment")
    radio_fields = {
        "cause": admin.VERTICAL,
        "perform_autopsy": admin.VERTICAL,
        "participant_hospitalized": admin.VERTICAL,
        "cause_category": admin.VERTICAL,
        "diagnosis_code": admin.VERTICAL,
        "medical_responsibility": admin.VERTICAL,
        "reason_hospitalized": admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Death",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalDeathReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalDeathReport, MaternalDeathReportAdmin)
