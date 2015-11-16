from django import forms

from edc_constants.constants import NOT_APPLICABLE

from ..models import AntenatalEnrollment

from .base_enrollment_form import BaseEnrollmentForm


class AntenatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        # If weeks of gestation are greater than 32 weeks, do a rapid test
        if cleaned_data.get('weeks_of_gestation') >= 32:
            if cleaned_data.get('process_rapid_test') == NOT_APPLICABLE:
                raise forms.ValidationError('Weeks of gestation are greater or equal to 32. Rapid test processing '
                                            'CANNOT be Not Applicable (Rapid test is expected). Please correct.')

        if cleaned_data.get('verbal_hiv_status') == 'NEVER' or cleaned_data.get('UNK') or cleaned_data.get('REFUSED'):
            if not cleaned_data.get('process_rapid_test') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'If the current HIV status is Never tested or Unknown or participant refused to answer then rapid test '
                    'is Not applicable.')
        if cleaned_data.get('valid_regimen') == 'Yes' and not cleaned_data.get('valid_regimen_duration') == 'No':
            raise forms.ValidationError('If the mothers HIV status is known then participant regimen validity should be No')

        if cleaned_data.get('process_rapid_test') == 'Yes' and not cleaned_data.get('date_of_rapid_test'):
            raise self.forms.ValidationError("If a Rapid Test was processed then please add date of rapid test.")
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        return cleaned_data

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
