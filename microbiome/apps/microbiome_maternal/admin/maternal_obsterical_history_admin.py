from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

from ..forms import MaternalObstericalHistoryForm
from ..models import MaternalObstericalHistory, MaternalVisit


class MaternalObstericalHistoryAdmin(BaseModelAdmin):

    form = MaternalObstericalHistoryForm
    fields = ('maternal_visit',
              'prev_pregnancies',
              'pregs_24wks_or_more',
              'lost_before_24wks',
              'lost_after_24wks',
              'live_children',
              'children_died_b4_5yrs')
    list_display = ('maternal_visit',
                    'prev_pregnancies',
                    'pregs_24wks_or_more',
                    'lost_before_24wks',
                    'lost_after_24wks',
                    'live_children')

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Obsterical History",
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
        return super(MaternalObstericalHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalObstericalHistory, MaternalObstericalHistoryAdmin)
