from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalUninfectedForm
from ..models import MaternalUninfected


class MaternalUninfectedAdmin(BaseModelAdmin):

    form = MaternalUninfectedForm
    fields = ('recruit_source',
              'recruit_source_other',
              'recruitment_clinic',
              'recruitment_clinic_other',
              'prev_pregnancies',
              'weight',
              'height',
              'systolic_bp',
              'diastolic_bp')
    list_display = ('recruit_source',
                    'recruitment_clinic',
                    'prev_pregnancies', )
    list_filter = ('recruit_source',
                   'recruitment_clinic',
                   'prev_pregnancies')
    radio_fields = {'recruit_source': admin.VERTICAL,
                    'recruitment_clinic': admin.VERTICAL}
admin.site.register(MaternalUninfected, MaternalUninfectedAdmin)
