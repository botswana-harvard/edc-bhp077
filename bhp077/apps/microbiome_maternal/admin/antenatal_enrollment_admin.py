from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import AntenatalEnrollmentForm
from ..models import AntenatalEnrollment


class AntenatalEnrollmentAdmin(BaseModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalEnrollmentForm

    fields = ('registered_subject',
              'report_datetime',
              'weeks_of_gestation',
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
    radio_fields = {'is_diabetic': admin.VERTICAL,
                    'on_tb_treatment': admin.VERTICAL,
                    'breastfeed_for_a_year': admin.VERTICAL,
                    'instudy_for_a_year': admin.VERTICAL,
                    'verbal_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'valid_regimen': admin.VERTICAL,
                    'process_rapid_test': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL}
    list_display = ('registered_subject', 'report_datetime', 'evidence_hiv_status',
                    'valid_regimen')
admin.site.register(AntenatalEnrollment, AntenatalEnrollmentAdmin)
