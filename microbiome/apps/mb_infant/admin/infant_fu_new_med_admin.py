from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_base.modeladmin.admin import BaseTabularInline
from edc_export.actions import export_as_csv_action

from ..forms import InfantFuNewMedItemsForm, InfantFuNewMedForm
from ..models import InfantFuNewMed, InfantFuNewMedItems
from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantFuNewMedItemsInline(BaseTabularInline):

    model = InfantFuNewMedItems
    form = InfantFuNewMedItemsForm
    extra = 0


class InfantFuNewMedItemsAdmin(BaseModelAdmin):

    form = InfantFuNewMedItemsForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Followup New Medications with meds list",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_fu_med__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_fu_med__infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_fu_med__infant_visit__appointment__registered_subject__dob',
                 'new_medications': 'infant_fu_med__new_medications',
                 }),
        )]
admin.site.register(InfantFuNewMedItems, InfantFuNewMedItemsAdmin)


class InfantFuNewMedAdmin(BaseInfantScheduleModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }
    inlines = [InfantFuNewMedItemsInline, ]
    form = InfantFuNewMedForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Followup New Medications",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_visit__appointment__registered_subject__dob',
                 }),
        )]

admin.site.register(InfantFuNewMed, InfantFuNewMedAdmin)
