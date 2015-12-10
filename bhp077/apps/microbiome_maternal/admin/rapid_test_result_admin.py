from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

from ..models import RapidTestResult, MaternalVisit


class RapidTestResultAdmin(BaseModelAdmin):
    fields = ('maternal_visit',
              'rapid_test_done',
              'rapid_test_date',
              'rapid_test_result',
              'comments')
    list_display = ('maternal_visit',
                    'rapid_test_done',
                    'rapid_test_result')
    list_filter = ('rapid_test_done', 'rapid_test_result')
    search_fields = ('rapid_test_date', )
    radio_fields = {"rapid_test_done": admin.VERTICAL,
                    "rapid_test_result": admin.VERTICAL, }

    actions = [
        export_as_csv_action(
            description="CSV Export of Rapid Test Result",
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
        return super(RapidTestResultAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(RapidTestResult, RapidTestResultAdmin)
