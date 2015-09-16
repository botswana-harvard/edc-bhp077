from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalClinicalHistoryForm
from ..models import MaternalClinicalHistory
from .site import admin_site


class MaternalClinicalHistoryAdmin(BaseModelAdmin):

    form = MaternalClinicalHistoryForm
    fields = ('prev_preg_azt',
              'prev_sdnvp_labour',
              'prev_preg_haart',
              'cd4_count',
              'cd4_date',
              'is_date_estimated',
              'comment')
    list_display = ('prev_preg_azt',
                    'prev_sdnvp_labour',
                    'prev_preg_haart',
                    'cd4_count',
                    'cd4_date')
    list_filter = ('prev_preg_azt',
                   'prev_sdnvp_labour',
                   'prev_preg_haart')
    radio_fields = {'prev_preg_azt': admin.VERTICAL,
                    'prev_sdnvp_labour': admin.VERTICAL,
                    'prev_preg_haart': admin.VERTICAL}
admin_site.register(MaternalClinicalHistory, MaternalClinicalHistoryAdmin)
