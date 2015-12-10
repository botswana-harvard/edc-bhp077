from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from edc.export.actions import export_as_csv_action

from ..forms import InfantFuImmunizationsForm
from ..models import InfantFuImmunizations, VaccinesReceived, VaccinesMissed


class VaccinesReceivedInlineAdmin(BaseTabularInline):
    model = VaccinesReceived
    extra = 1


class VaccinesMissedInlineAdmin(BaseTabularInline):
    model = VaccinesMissed
    extra = 1


class InfantFuImmunizationsAdmin(BaseModelAdmin):
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
