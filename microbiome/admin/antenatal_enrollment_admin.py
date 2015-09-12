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
              'verbal_hiv_status',
              'evidence_hiv_status',
              'valid_regime',
              'process_rapid_test',
              'date_of_rapid_test',
              'rapid_test_result')
    radio_fields = {'verbal_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'valid_regime': admin.VERTICAL,
                    'process_rapid_test': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL}
admin_site.register(AntenatalEnrollment, AntenatalEnrollmentAdmin)
