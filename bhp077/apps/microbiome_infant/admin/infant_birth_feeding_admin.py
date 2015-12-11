from collections import OrderedDict

from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin
from edc.base.modeladmin.admin import BaseTabularInline
from edc.export.actions import export_as_csv_action

from ..models import InfantBirthFeedVaccine, InfantVaccines
from ..forms import InfantVaccinesForm, InfantBirthFeedVaccineForm

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantVaccinesInline(BaseTabularInline):

    model = InfantVaccines
    form = InfantVaccinesForm
    extra = 0


class InfantBirthFeedVaccineAdmin(BaseInfantScheduleModelAdmin):
    form = InfantBirthFeedVaccineForm

    list_display = ('feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    inlines = [InfantVaccinesInline]

    radio_fields = {'feeding_after_delivery': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth Feeding & Vaccination",
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

admin.site.register(InfantBirthFeedVaccine, InfantBirthFeedVaccineAdmin)


class InfantVaccinesAdmin(BaseModelAdmin):
    form = InfantVaccinesForm
admin.site.register(InfantVaccines, InfantVaccinesAdmin)
