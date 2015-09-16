from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalMedicalHistoryForm
from ..models import MaternalMedicalHistory
from .site import admin_site


class MaternalMedicalHistoryAdmin(BaseModelAdmin):

    form = MaternalMedicalHistoryForm
    fields = ('has_chronic_cond',
              'chronic_cond',
              'chronic_cond_other',
              'who_diagnosis')
    list_display = ('has_chronic_cond', )
    list_filter = ('has_chronic_cond', )
    radio_fields = {'has_chronic_cond': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL}
    filter_horizontal = ('chronic_cond',)
admin_site.register(MaternalMedicalHistory, MaternalMedicalHistoryAdmin)
