from django.contrib import admin

from .registered_subject_model_admin import RegisteredSubjectModelAdmin

from ..forms import PostnatalEnrollmentForm
from ..models import PostnatalEnrollment


class PostnatalEnrollmentAdmin(RegisteredSubjectModelAdmin):

    form = PostnatalEnrollmentForm

    fields = ('report_datetime',
              'postpartum_days',
              'delivery_type',
              'gestation_before_birth',
              'live_or_still_birth',
              'live_infants',
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
    radio_fields = {'delivery_type': admin.VERTICAL,
                    'live_or_still_birth': admin.VERTICAL,
                    'citizen': admin.VERTICAL,
                    'is_diabetic': admin.VERTICAL,
                    'on_tb_treatment': admin.VERTICAL,
                    'breastfeed_for_a_year': admin.VERTICAL,
                    'instudy_for_a_year': admin.VERTICAL,
                    'verbal_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'valid_regimen': admin.VERTICAL,
                    'process_rapid_test': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL}
admin.site.register(PostnatalEnrollment, PostnatalEnrollmentAdmin)
