from django.contrib import admin
from django import forms

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.subject.registration.models import RegisteredSubject

from ..forms import PostnatalEnrollmentForm
from ..models import PostnatalEnrollment, AntenatalEnrollment


class PostnatalEnrollmentAdmin(BaseModelAdmin):

    fields = [
        'registered_subject', 'report_datetime', 'postpartum_days', 'vaginal_delivery', 'gestation_wks_delivered',
        'delivery_status', 'live_infants', 'is_diabetic', 'on_tb_tx', 'on_hypertension_tx',
        'will_breastfeed', 'will_remain_onstudy', 'week32_test', 'week32_test_date', 'week32_result',
        'current_hiv_status', 'evidence_hiv_status', 'valid_regimen', 'valid_regimen_duration', 'rapid_test_done',
        'rapid_test_date', 'rapid_test_result'
    ]

    form = PostnatalEnrollmentForm
    dashboard_type = 'maternal'

    def antenatal_enrollment(self, registered_subject):
        try:
            return AntenatalEnrollment.objects.get(
                registered_subject=registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return False

    def exclude_fields(self):
        exclude = ['is_diabetic', 'on_tb_tx', 'on_hypertension_tx', 'will_breastfeed',
                   'will_remain_onstudy', 'week32_test', 'week32_test_date', 'week32_result', 'current_hiv_status',
                   'valid_regimen', 'valid_regimen_duration', 'rapid_test_done', 'rapid_test_date',
                   'rapid_test_result', 'valid_regimen', 'evidence_hiv_status']
        return exclude

    def disable_fields(self, form):
        for field in self.exclude_fields():
            form.base_fields[field].widget.attrs['disabled'] = 'disabled'

    def hide_fields(self, form):
        for field in self.exclude_fields():
            form.base_fields[field].widget = forms.HiddenInput()

    def update_postnatal(self, form, antenatal):

        form.base_fields['is_diabetic'].initial = antenatal.is_diabetic
        form.base_fields['on_tb_tx'].initial = antenatal.on_tb_tx
        form.base_fields['on_hypertension_tx'].initial = antenatal.on_hypertension_tx
        form.base_fields['will_breastfeed'].initial = antenatal.will_breastfeed
        form.base_fields['will_remain_onstudy'].initial = antenatal.will_remain_onstudy
        form.base_fields['week32_test'].initial = antenatal.week32_test
        form.base_fields['week32_test_date'].initial = antenatal.week32_test_date
        form.base_fields['week32_result'].initial = antenatal.week32_result
        form.base_fields['current_hiv_status'].initial = antenatal.current_hiv_status
        form.base_fields['valid_regimen'].initial = antenatal.valid_regimen
        form.base_fields['evidence_hiv_status'].initial = antenatal.evidence_hiv_status
        form.base_fields['valid_regimen_duration'].initial = antenatal.valid_regimen_duration
        form.base_fields['rapid_test_done'].initial = antenatal.rapid_test_done
        form.base_fields['rapid_test_date'].initial = antenatal.rapid_test_date
        form.base_fields['rapid_test_result'].initial = antenatal.rapid_test_result
        form.base_fields['valid_regimen'].initial = antenatal.valid_regimen
        return form

    def get_form(self, request, obj=None, **kwargs):
        form = super(PostnatalEnrollmentAdmin, self).get_form(request, obj, **kwargs)
        antenatal = None
        try:
            registered_subject = RegisteredSubject.objects.get(id=request.GET.get('registered_subject', None))
            if self.antenatal_enrollment(registered_subject):
                antenatal = self.antenatal_enrollment(registered_subject)
            if antenatal:
                if not obj:
                    form = self.update_postnatal(form, antenatal)
                    self.hide_fields(form)
                else:
                    self.disable_fields(form)
        except RegisteredSubject.DoesNotExist:
            pass
        return form

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
    list_display = ('registered_subject', 'report_datetime', 'vaginal_delivery',
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
