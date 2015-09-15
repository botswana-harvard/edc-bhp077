from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import AntenatalEnrollmentForm
from ..models import AntenatalEnrollment

from .site import admin_site


class AntenatalEnrollmentAdmin(BaseModelAdmin):

    form = AntenatalEnrollmentForm

    fields = ('maternal_consent',
              'report_datetime',
              'weeks_of_gestation',
              'citizen',
              'is_diabetic',
              'on_tb_treatment',
              'breastfeed_for_a_year',
              'instudy_for_a_year',
              'verbal_hiv_status',
              'evidence_hiv_status',
              'valid_regimen',
              'process_rapid_test',
              'date_of_rapid_test',
              'rapid_test_result')
    radio_fields = {'citizen': admin.VERTICAL,
                    'is_diabetic': admin.VERTICAL,
                    'on_tb_treatment': admin.VERTICAL,
                    'breastfeed_for_a_year': admin.VERTICAL,
                    'instudy_for_a_year': admin.VERTICAL,
                    'verbal_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'valid_regimen': admin.VERTICAL,
                    'process_rapid_test': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL}
admin_site.register(AntenatalEnrollment, AntenatalEnrollmentAdmin)
