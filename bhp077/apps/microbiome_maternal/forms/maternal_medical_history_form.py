from django import forms

from edc_constants.choices import NEG, YES

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalMedicalHistory, PostnatalEnrollment


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

        self.who_stage_diagnosis_for_neg_mother()
        self.validate_has_chronic_condition_no_listing()
        self.chronic_condition_on_enrollment()
        self.validate_has_who_diagnosis_no_listing()
        return cleaned_data

    def validate_has_chronic_condition_no_listing(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('chronic_cond_since') == YES:
            if not cleaned_data.get('chronic_cond'):
                raise forms.ValidationError(
                    "You mentioned there are chronic conditions. Please list them.")

    def validate_has_who_diagnosis_no_listing(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('who_diagnosis') == YES:
            if not cleaned_data.get('wcs_dx_adult'):
                raise forms.ValidationError(
                    "You mentioned participant has WHO diagnosis. Please list them.")

    def who_stage_diagnosis_for_neg_mother(self):
        """Confirms the NEG HIV status of a mother and throws
        validation error on WHO stage selection """
        cleaned_data = self.cleaned_data
        try:
            postnatal_enrollment = PostnatalEnrollment.objects.get(
                registered_subject=cleaned_data.get('maternal_visit').appointment.registered_subject)
            if postnatal_enrollment.enrollment_hiv_status == NEG:
                if cleaned_data.get('who_diagnosis') == YES:
                    raise forms.ValidationError("Mother is NEG. WHO stage diagnosis should be No.")
        except PostnatalEnrollment.DoesNotExist:
            pass

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'
