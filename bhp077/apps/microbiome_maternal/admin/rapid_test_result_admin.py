from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..models import RapidTestResult


class RapidTestResultAdmin(BaseModelAdmin):
    fields = ('maternal_visit',
              'process_rapid_test',
              'date_of_rapid_test',
              'rapid_test_result',
              'comments')
    list_display = ('maternal_visit',
                    'process_rapid_test',
                    'rapid_test_result')
    list_filter = ('process_rapid_test', 'rapid_test_result')
    search_fields = ('date_of_rapid_test', )
    radio_fields = {"process_rapid_test": admin.VERTICAL,
                    "rapid_test_result": admin.VERTICAL, }
admin.site.register(RapidTestResult, RapidTestResultAdmin)
