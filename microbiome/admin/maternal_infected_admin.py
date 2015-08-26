from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalInfectedForm
from ..models import MaternalInfected
from .site import admin_site


class MaternalInfectedAdmin(BaseModelAdmin):

    form = MaternalInfectedForm
    fields = ('recruit_source',
              'recruit_source_other',
              'recruitment_clinic',
              'recruitment_clinic_other',
              'prev_pregnancies',
              'prior_health_haart',
              'prev_pregnancy_arv',
              'weight',
              'height',
              'bp')
    list_display = ('recruit_source',
                    'recruitment_clinic',
                    'prev_pregnancies',
                    'prior_health_haart',
                    'prev_pregnancy_arv')
    list_filter = ('recruit_source',
                   'recruitment_clinic',
                   'prev_pregnancies',
                   'prior_health_haart',
                   'prev_pregnancy_arv')
    radio_fields = {'recruit_source': admin.VERTICAL,
                    'recruitment_clinic': admin.VERTICAL,
                    'prior_health_haart': admin.VERTICAL,
                    'prev_pregnancy_arv': admin.VERTICAL}
admin_site.register(MaternalInfected, MaternalInfectedAdmin)
