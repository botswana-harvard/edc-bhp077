from django.contrib import admin

from ..forms import MaternalClinicalHistoryForm
from ..models import MaternalClinicalHistory

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalClinicalHistoryAdmin(BaseMaternalModelAdmin):

    form = MaternalClinicalHistoryForm
    fields = ('maternal_visit',
              'prev_preg_azt',
              'prev_sdnvp_labour',
              'prev_preg_haart',
              'lowest_cd4_known',
              'cd4_count',
              'cd4_date',
              'is_date_estimated',
              'comment',
              'prior_health_haart',
              'prev_pregnancy_arv',
              'know_hiv_status',)

    list_display = ('maternal_visit',
                    'prev_preg_azt',
                    'prev_sdnvp_labour',
                    'prev_preg_haart',
                    'lowest_cd4_known',
                    'cd4_count',
                    'cd4_date')

    list_filter = ('prev_preg_azt',
                   'prev_sdnvp_labour',
                   'prev_preg_haart',
                   'prior_health_haart',
                   'prev_pregnancy_arv',)

    radio_fields = {'prev_preg_azt': admin.VERTICAL,
                    'prev_sdnvp_labour': admin.VERTICAL,
                    'prev_preg_haart': admin.VERTICAL,
                    'lowest_cd4_known': admin.VERTICAL,
                    'is_date_estimated': admin.VERTICAL,
                    'prior_health_haart': admin.VERTICAL,
                    'prev_pregnancy_arv': admin.VERTICAL,
                    'know_hiv_status': admin.VERTICAL}

admin.site.register(MaternalClinicalHistory, MaternalClinicalHistoryAdmin)
