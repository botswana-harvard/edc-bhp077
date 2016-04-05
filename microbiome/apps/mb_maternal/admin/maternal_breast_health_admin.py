from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import MaternalBreastHealthForm
from ..models import MaternalBreastHealth

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalBreastHealthAdmin(BaseMaternalModelAdmin):

    form = MaternalBreastHealthForm

    radio_fields = {
        "breast_feeding": admin.VERTICAL,
        "has_mastitis": admin.VERTICAL,
        "mastitis": admin.VERTICAL,
        "has_lesions": admin.VERTICAL,
        "lesions": admin.VERTICAL,
        "advised_stop_bf": admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Breast Health",
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

admin.site.register(MaternalBreastHealth, MaternalBreastHealthAdmin)
