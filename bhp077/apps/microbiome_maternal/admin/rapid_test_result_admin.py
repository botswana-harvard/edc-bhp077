from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..models import RapidTestResult, MaternalVisit


class RapidTestResultAdmin(BaseModelAdmin):
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(RapidTestResultAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(RapidTestResult, RapidTestResultAdmin)
