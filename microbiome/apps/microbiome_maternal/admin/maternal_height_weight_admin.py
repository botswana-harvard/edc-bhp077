from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

from ..forms import MaternalHeightWeightForm
from ..models import MaternalHeightWeight, MaternalVisit


class MaternalHeightWeightAdmin(BaseModelAdmin):

    form = MaternalHeightWeightForm
    fields = ('maternal_visit',
              'weight_kg',
              'height',
              'systolic_bp',
              'diastolic_bp')

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Height and Weight",
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
        return super(MaternalHeightWeightAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(MaternalHeightWeight, MaternalHeightWeightAdmin)
