from django import forms

from edc_constants.constants import NEG, YES

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalMedicalHistory, PostnatalEnrollment


class MaternalMedicalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalMedicalHistoryForm, self).clean()
        if 'chronic' in cleaned_data.keys():
            self.validate_m2m(
                label='chronic condition',
                leading=cleaned_data.get('chronic_since'),
                m2m=cleaned_data.get('chronic'),
                other=cleaned_data.get('chronic_other'))
        # WHO validations
        if 'who' in cleaned_data.keys():
            self.validate_m2m_wcs_dx(
                label='WHO diagnoses',
                leading=cleaned_data.get('who_diagnosis'),
                m2m=cleaned_data.get('who'))

        self.who_stage_diagnosis_for_neg_mother()
        self.validate_has_chronicition_no_listing()
        self.validate_has_who_diagnosis_no_listing()
        return cleaned_data

    def validate_has_chronicition_no_listing(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('chronic_since') == YES:
            if not cleaned_data.get('chronic'):
                raise forms.ValidationError(
                    "You mentioned there are chronic conditions. Please list them.")

    def validate_has_who_diagnosis_no_listing(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('who_diagnosis') == YES:
            if not cleaned_data.get('who'):
                raise forms.ValidationError(
                    "You mentioned participant has WHO diagnosis. Please list them.")

    def who_stage_diagnosis_for_neg_mother(self):
        """Confirms the NEG HIV status of a mother and throws
        validation error on WHO stage selection """
        cleaned_data = self.cleaned_data
        try:
            postnatal_enrollment = PostnatalEnrollment.objects.get(
                registered_subject=cleaned_data.get(
                    'maternal_visit').appointment.registered_subject)
            if postnatal_enrollment.enrollment_hiv_status == NEG:
                if cleaned_data.get('who_diagnosis') == YES:
                    raise forms.ValidationError(
                        "Mother is NEG. WHO stage diagnosis should be No.")
        except PostnatalEnrollment.DoesNotExist:
            pass

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'
