from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalMedicalHistoryForm
from ..models import MaternalMedicalHistory, MaternalVisit


class MaternalMedicalHistoryAdmin(BaseModelAdmin):

    form = MaternalMedicalHistoryForm
    fields = ('maternal_visit',
              'chronic_cond_since',
              'chronic_cond',
              'chronic_cond_other',
              'who_diagnosis',
              'wcs_dx_adult')
    list_display = ('maternal_visit', 'chronic_cond_since', )
    list_filter = ('chronic_cond_since', )
    radio_fields = {'chronic_cond_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL}
    filter_horizontal = ('chronic_cond', 'wcs_dx_adult',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalMedicalHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalMedicalHistory, MaternalMedicalHistoryAdmin)
