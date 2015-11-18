from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalClinicalHistoryForm
from ..models import MaternalClinicalHistory, MaternalVisit


class MaternalClinicalHistoryAdmin(BaseModelAdmin):

    form = MaternalClinicalHistoryForm
    fields = ('maternal_visit',
              'prev_preg_azt',
              'prev_sdnvp_labour',
              'prev_preg_haart',
              'lowest_cd4_known',
              'cd4_count',
              'cd4_date',
              'is_date_estimated',
              'comment')
    list_display = ('maternal_visit',
                    'prev_preg_azt',
                    'prev_sdnvp_labour',
                    'prev_preg_haart',
                    'lowest_cd4_known',
                    'cd4_count',
                    'cd4_date')
    list_filter = ('prev_preg_azt',
                   'prev_sdnvp_labour',
                   'prev_preg_haart')
    radio_fields = {'prev_preg_azt': admin.VERTICAL,
                    'prev_sdnvp_labour': admin.VERTICAL,
                    'prev_preg_haart': admin.VERTICAL,
                    'lowest_cd4_known': admin.VERTICAL,
                    'is_date_estimated': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalClinicalHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalClinicalHistory, MaternalClinicalHistoryAdmin)
