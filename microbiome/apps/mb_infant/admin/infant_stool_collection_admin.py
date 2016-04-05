from collections import OrderedDict

from django.contrib import admin

from edc_admin_exclude import AdminExcludeFieldsMixin
from edc_export.actions import export_as_csv_action

from ..forms import InfantStoolCollectionForm
from ..models import InfantStoolCollection, InfantVisit

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantStoolCollectionAdmin(AdminExcludeFieldsMixin, BaseInfantScheduleModelAdmin):

    visit_model = InfantVisit
    visit_attr = 'infant_visit'
    visit_codes = {'visit': ['2000']}

    fields = ('infant_visit',
              'report_datetime',
              'sample_obtained',
              'nappy_type',
              'other_nappy',
              'stool_collection',
              'stool_collection_time',
              'stool_stored',
              'past_diarrhea',
              'diarrhea_past_24hrs',
              'antibiotics_7days',
              'antibiotic_dose_24hrs',)

    form = InfantStoolCollectionForm
    radio_fields = {
        "sample_obtained": admin.VERTICAL,
        "nappy_type": admin.VERTICAL,
        "stool_collection": admin.VERTICAL,
        "stool_stored": admin.VERTICAL,
        "past_diarrhea": admin.VERTICAL,
        "diarrhea_past_24hrs": admin.VERTICAL,
        "antibiotics_7days": admin.VERTICAL,
        "antibiotic_dose_24hrs": admin.VERTICAL}

    custom_exclude = {'visit': ['past_diarrhea', 'diarrhea_past_24hrs',
                                'antibiotics_7days', 'antibiotic_dose_24hrs']}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Stool Collection",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantStoolCollectionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantStoolCollection, InfantStoolCollectionAdmin)
