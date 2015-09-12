from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import PostnatalEnrollmentForm
from ..models import PostnatalEnrollment

from .site import admin_site


class PostnatalEnrollmentAdmin(BaseModelAdmin):

    form = PostnatalEnrollmentForm

    fields = ('maternal_consent',
              'report_datetime',
              'postpartum_days',
              'delivery_type',
              'live_or_still_birth',
              'live_infants',
              'verbal_hiv_status',
              'evidence_hiv_status',
              'valid_regime',
              'process_rapid_test',
              'date_of_rapid_test',
              'rapid_test_result')
    radio_fields = {'delivery_type': admin.VERTICAL,
                    'live_or_still_birth': admin.VERTICAL,
                    'verbal_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'valid_regime': admin.VERTICAL,
                    'process_rapid_test': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL}
admin_site.register(PostnatalEnrollment, PostnatalEnrollmentAdmin)
