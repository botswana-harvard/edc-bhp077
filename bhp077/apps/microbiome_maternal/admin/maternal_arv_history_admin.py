from collections import OrderedDict

from django.contrib import admin

from edc.export.actions import export_as_csv_action

from ..models import MaternalArvHistory
from ..forms import MaternalArvHistoryForm

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalArvHistoryAdmin(BaseMaternalModelAdmin):
    form = MaternalArvHistoryForm

    list_display = ('haart_start_date', 'preg_on_haart')

    list_filter = ('preg_on_haart', )

    radio_fields = {
        'preg_on_haart': admin.VERTICAL,
        'prior_preg': admin.VERTICAL,
        'is_date_estimated': admin.VERTICAL}

    filter_horizontal = ('prior_arv', )

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal ARV History",
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

admin.site.register(MaternalArvHistory, MaternalArvHistoryAdmin)
