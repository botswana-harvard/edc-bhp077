from collections import OrderedDict

from django.contrib import admin

from edc.subject.off_study.admin import BaseOffStudyModelAdmin
from edc.export.actions import export_as_csv_action

from ..models import MaternalOffStudy, MaternalVisit
from ..forms import MaternalOffStudyForm


class MaternalOffStudyAdmin(BaseOffStudyModelAdmin):
    form = MaternalOffStudyForm
    dashboard_type = 'maternal'
    visit_model_name = 'maternalvisit'

    fields = (
        'registered_subject',
        'maternal_visit',
        'offstudy_date',
        'reason',
        'reason_other',
        'has_scheduled_data',
        'comment')

    radio_fields = {
        "has_scheduled_data": admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Off Study",
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

        return super(MaternalOffStudyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalOffStudy, MaternalOffStudyAdmin)
