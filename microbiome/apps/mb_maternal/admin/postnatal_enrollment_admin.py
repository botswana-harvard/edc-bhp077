from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.subject.registration.models import RegisteredSubject
from edc.export.actions import export_as_csv_action

from ..forms import PostnatalEnrollmentForm
from ..models import PostnatalEnrollment, AntenatalEnrollment


class PostnatalEnrollmentAdmin(BaseModelAdmin):

    form = PostnatalEnrollmentForm

    dashboard_type = 'maternal'

    fields = [
        'registered_subject', 'report_datetime', 'postpartum_days', 'vaginal_delivery', 'gestation_wks_delivered',
        'delivery_status', 'live_infants', 'is_diabetic', 'on_tb_tx', 'on_hypertension_tx',
        'will_breastfeed', 'will_remain_onstudy', 'week32_test', 'week32_test_date', 'week32_result',
        'current_hiv_status', 'evidence_hiv_status', 'valid_regimen', 'valid_regimen_duration', 'rapid_test_done',
        'rapid_test_date', 'rapid_test_result'
    ]

    radio_fields = {'vaginal_delivery': admin.VERTICAL,
                    'delivery_status': admin.VERTICAL,
                    'is_diabetic': admin.VERTICAL,
                    'on_tb_tx': admin.VERTICAL,
                    'on_hypertension_tx': admin.VERTICAL,
                    'will_breastfeed': admin.VERTICAL,
                    'will_remain_onstudy': admin.VERTICAL,
                    'week32_test': admin.VERTICAL,
                    'week32_result': admin.VERTICAL,
                    'current_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'valid_regimen': admin.VERTICAL,
                    'valid_regimen_duration': admin.VERTICAL,
                    'rapid_test_done': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL}

    list_display = ('registered_subject', 'report_datetime', 'is_eligible', 'custom_enrollment_hiv_status',
                    'custom_vaginal_delivery', 'custom_current_hiv_status', 'custom_evidence_hiv_status',
                    'custom_valid_regimen', 'custom_week32_test', 'custom_rapid_test_done')

    list_filter = ('report_datetime', 'enrollment_hiv_status', 'is_eligible', 'vaginal_delivery',
                   'current_hiv_status', 'evidence_hiv_status', 'valid_regimen', 'valid_regimen_duration',
                   'week32_test', 'rapid_test_done')

    def custom_enrollment_hiv_status(self, obj):
        return obj.enrollment_hiv_status
    custom_enrollment_hiv_status.short_description = 'Enrollment'

    def custom_vaginal_delivery(self, obj):
        return obj.vaginal_delivery
    custom_vaginal_delivery.short_description = 'Vaginal'

    def custom_evidence_hiv_status(self, obj):
        return obj.evidence_hiv_status
    custom_evidence_hiv_status.short_description = 'Evidence'

    def custom_current_hiv_status(self, obj):
        return obj.current_hiv_status
    custom_current_hiv_status.short_description = 'Current'

    def custom_week32_test(self, obj):
        return obj.week32_test
    custom_week32_test.short_description = '32wks'

    def custom_rapid_test_done(self, obj):
        return obj.rapid_test_done
    custom_rapid_test_done.short_description = 'Rapid'

    def custom_valid_regimen(self, obj):
        return obj.valid_regimen
    custom_valid_regimen.short_description = 'Valid Regimen'

    def get_form(self, request, obj=None, **kwargs):
        """Updates the ADD form fields in a form from antenatal enrollment."""
        form = super(PostnatalEnrollmentAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            try:
                registered_subject = RegisteredSubject.objects.get(
                    id=request.GET.get('registered_subject', None))
                antenatal_enrollment = AntenatalEnrollment.objects.get(
                    registered_subject=registered_subject,
                    is_eligible=True)
                form = self.update_with_common_fields_from_antenatal_enrollment(
                    form, antenatal_enrollment)
            except RegisteredSubject.DoesNotExist:
                pass
            except AntenatalEnrollment.DoesNotExist:
                pass
        return form

    def update_with_common_fields_from_antenatal_enrollment(self, form, antenatal_enrollment):
        """Sets the form field value from antenatal enrollment for fields common between the
        two models."""
        try:
            for attrname in antenatal_enrollment.common_fields():
                form.base_fields[attrname].initial = getattr(antenatal_enrollment, attrname)
                # form.base_fields[attrname].widget.attrs['disabled'] = 'disabled'
        except AntenatalEnrollment.DoesNotExist:
            pass
        return form

#     def disable_fields(self, form):
#         for field in self.exclude_fields():
#             form.base_fields[field].widget.attrs['disabled'] = 'disabled'
#         return form
#
#     def hide_fields(self, form):
#         for field in self.exclude_fields():
#             form.base_fields[field].widget = forms.HiddenInput()
#         return form
#
#     def exclude_fields(self):
#         exclude = ['is_diabetic', 'on_tb_tx', 'on_hypertension_tx', 'will_breastfeed',
#                    'will_remain_onstudy', 'week32_test', 'week32_test_date', 'week32_result', 'current_hiv_status',
#                    'valid_regimen', 'valid_regimen_duration', 'rapid_test_done', 'rapid_test_date',
#                    'rapid_test_result', 'valid_regimen', 'evidence_hiv_status']
#         return exclude

    actions = [
        export_as_csv_action(
            description="CSV Export of Postnatal Enrollment",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 'registered': 'registered_subject__registration_datetime'}),
        )]

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
