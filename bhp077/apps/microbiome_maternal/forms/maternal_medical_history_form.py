from django import forms
from django.core.exceptions import ValidationError

from edc_constants.choices import NO

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalMedicalHistory
from ..models import AntenatalEnrollment
from ..models import PostnatalEnrollment


class MaternalMedicalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalMedicalHistoryForm, self).clean()
        if 'chronic_cond' in cleaned_data.keys():
            self.validate_m2m(
                label='chronic condition',
                leading=cleaned_data.get('chronic_cond_since'),
                m2m=cleaned_data.get('chronic_cond'),
                other=cleaned_data.get('chronic_cond_other'))
        # WHO validations
        if 'wcs_dx_adult' in cleaned_data.keys():
            self.validate_m2m_wcs_dx(
                label='WHO diagnoses',
                leading=cleaned_data.get('who_diagnosis'),
                m2m=cleaned_data.get('wcs_dx_adult'))
        self.compare_chronic_on_antenatal_postnatal_and_medical_history(forms.ValidationError)

        return cleaned_data

    def compare_chronic_on_antenatal_postnatal_and_medical_history(self, exception_cls=None):
        """Compares chronic diseases on antenatal, postnatal and maternal medical history."""
        cleaned_data = self.cleaned_data
        exception_cls = exception_cls or ValidationError
        chronic_diseases = cleaned_data.get('chronic_cond').all()
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(
                registered_subject=cleaned_data.get('maternal_visit').appointment.registered_subject
            )
            for chronic in chronic_diseases:
                if chronic.short_name == "Chronic Hypertention" and antenatal_enrollment.on_hypertension_tx == NO:
                    raise exception_cls('Its indicated that the participant has no chronic disease at antenatal enrollment,'
                                        'yet have indicated the participant has Chronic Hypertention on the medical history')
                elif chronic.short_name == "Chronic Diabetes" and antenatal_enrollment.is_diabetic == NO:
                    raise exception_cls('Its indicated that the participant has no chronic disease at antenatal enrollment,'
                                        'yet have indicated the participant has Chronic Diabetes on the medical history')
                elif chronic.short_name == "Tuberculosis" and antenatal_enrollment.on_tb_tx == NO:
                    raise exception_cls('Its indicated that the participant has no chronic disease at antenatal enrollment,'
                                        'yet have indicated the participant has Chronic Diabetes on the medical history')
        except AntenatalEnrollment.DoesNotExist:
            pass
        try:
            postnatal_enrollment = PostnatalEnrollment.objects.get(
                registered_subject=cleaned_data.get('maternal_visit').appointment.registered_subject
            )
            for chronic in chronic_diseases:
                if chronic.short_name == "Chronic Hypertention" and postnatal_enrollment.on_hypertension_tx == NO:
                    raise exception_cls('Its indicated that the participant has no chronic disease at postnatal enrollment,'
                                        'yet have indicated the participant has Chronic Hypertention on the medical history')
                elif chronic.short_name == "Chronic Diabetes" and postnatal_enrollment.is_diabetic == NO:
                    raise exception_cls('Its indicated that the participant has no chronic disease at postnatal enrollment,'
                                        'yet have indicated the participant has Chronic Diabetes on the medical history')
                elif chronic.short_name == "Tuberculosis" and postnatal_enrollment.on_tb_tx == NO:
                    raise exception_cls('Its indicated that the participant has no chronic disease at postnatal enrollment,'
                                        'yet have indicated the participant has Chronic Diabetes on the medical history')
        except PostnatalEnrollment.DoesNotExist:
            pass

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'
