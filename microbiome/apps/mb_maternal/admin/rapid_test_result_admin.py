from django.contrib import admin

from ..models import RapidTestResult

from .base_maternal_model_admin import BaseMaternalModelAdmin


class RapidTestResultAdmin(BaseMaternalModelAdmin):
    fields = ('maternal_visit',
              'rapid_test_done',
              'rapid_test_date',
              'result',
              'comments')
    list_display = ('maternal_visit',
                    'rapid_test_done',
                    'result')
    list_filter = ('rapid_test_done', 'result')
    search_fields = ('rapid_test_date', )
    radio_fields = {"rapid_test_done": admin.VERTICAL,
                    "result": admin.VERTICAL, }

admin.site.register(RapidTestResult, RapidTestResultAdmin)
