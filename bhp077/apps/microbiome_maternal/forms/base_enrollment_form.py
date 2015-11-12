from django import forms
from edc.base.form.forms import BaseModelForm

from edc_constants.constants import POS, NEG, NOT_APPLICABLE, YES

from ..models import BaseEnrollment


class BaseEnrollmentForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('verbal_hiv_status') == POS or cleaned_data.get('verbal_hiv_status') == NEG:
            if cleaned_data.get('evidence_hiv_status') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is {}, evidence'
                                            ' of HIV result cannot be Not Applicable. Please correct.'
                                            .format(cleaned_data.get('verbal_hiv_status')))
        if cleaned_data.get('verbal_hiv_status') == POS:
            if cleaned_data.get('valid_regimen') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Positive, "do records show that'
                                            ' participant takes ARVs" cannot be Not Applicable')
        else:
            if cleaned_data.get('valid_regimen') != NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is {}, "do records show that'
                                            'participant takes ARVs" cannot be {}. Please correct'
                                            .format(cleaned_data.get('verbal_hiv_status'),
                                                    cleaned_data.get('valid_regimen')))
        if cleaned_data.get('process_rapid_test') == YES:
            # date of rapid test is required if rapid test processed is indicated as Yes
            if not cleaned_data.get('date_of_rapid_test'):
                raise forms.ValidationError('You indicated that a rapid test was processed. Please provide the date.')
            # if rapid test was done, result should be indicated
            if not cleaned_data.get('rapid_test_result'):
                raise forms.ValidationError('You indicated that a rapid test was processed. Please provide a result.')
        else:
            if cleaned_data.get('date_of_rapid_test'):
                raise forms.ValidationError('You indicated that a rapid test was NOT processed, yet rapid test date was'
                                            ' provided. Please correct.')
            if cleaned_data.get('rapid_test_result'):
                raise forms.ValidationError('You indicated that a rapid test was NOT processed, yet rapid test result '
                                            'was provided. Please correct.')
        return super(BaseEnrollmentForm, self).clean()

    class Meta:
        model = BaseEnrollment
        fields = '__all__'
