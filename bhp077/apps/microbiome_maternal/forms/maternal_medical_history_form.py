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
        self.chronic_condition_on_enrollment()

        # HIV NEG, then cannot fill in a WHO diagnosis

        return cleaned_data

    def chronic_condition_on_enrollment(self):
        """Compares chronic diseases reported on the antenatal and postnatal enrollment."""
        cleaned_data = self.cleaned_data
        chronic_diseases = cleaned_data.get('chronic_cond').all()
        for EnrollmentModel in [AntenatalEnrollment, PostnatalEnrollment]:
            try:
                enrollment = EnrollmentModel.objects.get(
                    registered_subject=cleaned_data.get('maternal_visit').appointment.registered_subject)
                for chronic in chronic_diseases:
                    error_msg = (
                        'Participant reported no chronic disease at {}, '
                        'yet you are reporting the participant has {{}}.'.format(
                            enrollment._meta.verbose_name))
                    if chronic.short_name == "Chronic Hypertention" and enrollment.on_hypertension_tx == NO:
                        raise forms.ValidationError(error_msg.format(chronic.short_name))
                    elif chronic.short_name == "Chronic Diabetes" and enrollment.is_diabetic == NO:
                        raise forms.ValidationError(error_msg.format(chronic.short_name))
                    elif chronic.short_name == "Tuberculosis" and enrollment.on_tb_tx == NO:
                        raise forms.ValidationError(error_msg.format(chronic.short_name))
            except EnrollmentModel.DoesNotExist:
                pass

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'
