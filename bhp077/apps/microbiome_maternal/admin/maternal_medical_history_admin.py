from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalMedicalHistoryForm
from ..models import MaternalMedicalHistory


class MaternalMedicalHistoryAdmin(BaseModelAdmin):

    form = MaternalMedicalHistoryForm
    fields = ('maternal_visit',
              'has_chronic_cond',
              'chronic_cond',
              'chronic_cond_other',
              'who_diagnosis')
    list_display = ('maternal_visit', 'has_chronic_cond', )
    list_filter = ('has_chronic_cond', )
    radio_fields = {'has_chronic_cond': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL}
    filter_horizontal = ('chronic_cond',)
admin.site.register(MaternalMedicalHistory, MaternalMedicalHistoryAdmin)
