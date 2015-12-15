from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

from ..forms import MaternalMedicalHistoryForm
from ..models import MaternalMedicalHistory, MaternalVisit


class MaternalMedicalHistoryAdmin(BaseModelAdmin):

    form = MaternalMedicalHistoryForm
    fields = ('maternal_visit',
              'chronic_since',
              'chronic',
              'chronic_other',
              'who_diagnosis',
              'who')
    list_display = ('maternal_visit', 'chronic_since', )
    list_filter = ('chronic_since', )
    radio_fields = {'chronic_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL}
    filter_horizontal = ('chronic', 'who',)

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Medical History",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 'registered': 'maternal_visit__appointment__registered_subject__registration_datetime'}),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalMedicalHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalMedicalHistory, MaternalMedicalHistoryAdmin)
