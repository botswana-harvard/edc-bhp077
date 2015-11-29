from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.subject.registration.models import RegisteredSubject

from ..forms import PostnatalEnrollmentForm
from ..models import PostnatalEnrollment


class PostnatalEnrollmentAdmin(BaseModelAdmin):

    dashboard_type = 'maternal'

    form = PostnatalEnrollmentForm

    fields = ('registered_subject',
              'report_datetime',
              'postpartum_days',
              'delivery_type',
              'gestation_before_birth',
              'live_or_still_birth',
              'live_infants',
              'is_diabetic',
              'on_tb_treatment',
              'on_hypertension_treatment',
              'breastfeed_for_a_year',
              'instudy_for_a_year',
              'week32_test',
              'week32_result',
              'verbal_hiv_status',
              'evidence_hiv_status',
              'valid_regimen',
              'valid_regimen_duration',
              'process_rapid_test',
              'date_of_rapid_test',
              'rapid_test_result')
    radio_fields = {'delivery_type': admin.VERTICAL,
                    'live_or_still_birth': admin.VERTICAL,
                    'is_diabetic': admin.VERTICAL,
                    'on_tb_treatment': admin.VERTICAL,
                    'on_hypertension_treatment': admin.VERTICAL,
                    'breastfeed_for_a_year': admin.VERTICAL,
                    'instudy_for_a_year': admin.VERTICAL,
                    'week32_test': admin.VERTICAL,
                    'week32_result': admin.VERTICAL,
                    'verbal_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'valid_regimen': admin.VERTICAL,
                    'valid_regimen_duration': admin.VERTICAL,
                    'process_rapid_test': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL}
    list_display = ('registered_subject', 'report_datetime', 'delivery_type',
                    'evidence_hiv_status', 'valid_regimen')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    id__exact=request.GET.get('registered_subject', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('registered_subject')
                except ValueError:
                    self.readonly_fields.append('registered_subject')
        return super(PostnatalEnrollmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(PostnatalEnrollment, PostnatalEnrollmentAdmin)
