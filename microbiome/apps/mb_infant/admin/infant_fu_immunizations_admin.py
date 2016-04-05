from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from edc_export.actions import export_as_csv_action

from ..forms import InfantFuImmunizationsForm, VaccinesReceivedForm, VaccinesMissedForm
from ..models import InfantFuImmunizations, VaccinesReceived, VaccinesMissed
from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class VaccinesReceivedInlineAdmin(BaseTabularInline):
    model = VaccinesReceived
    form = VaccinesReceivedForm
    extra = 1


class VaccinesMissedInlineAdmin(BaseTabularInline):
    model = VaccinesMissed
    form = VaccinesMissedForm
    extra = 1


class VaccinesReceivedAdmin(BaseModelAdmin):
    form = VaccinesReceivedForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Immunizations with vaccines received",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_fu_immunizations__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_fu_immunizations__infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_fu_immunizations__infant_visit__appointment__registered_subject__dob',
                 'vaccines_received': 'infant_fu_immunizations__vaccines_received'
                 }),
        )]


class VaccinesMissedAdmin(BaseModelAdmin):
    form = VaccinesMissedForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Immunizations with vaccines missed",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_fu_immunizations__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_fu_immunizations__infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_fu_immunizations__infant_visit__appointment__registered_subject__dob',
                 'vaccines_missed': 'infant_fu_immunizations__vaccines_missed'
                 }),
        )]


class InfantFuImmunizationsAdmin(BaseInfantScheduleModelAdmin):
    form = InfantFuImmunizationsForm
    inlines = [VaccinesReceivedInlineAdmin, VaccinesMissedInlineAdmin, ]
    radio_fields = {'vaccines_received': admin.VERTICAL,
                    'vaccines_missed': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Immunizations",
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

admin.site.register(InfantFuImmunizations, InfantFuImmunizationsAdmin)
