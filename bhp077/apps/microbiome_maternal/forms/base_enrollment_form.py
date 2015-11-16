from django import forms
from edc.base.form.forms import BaseModelForm

from edc_constants.constants import POS, NEG, NOT_APPLICABLE, YES

from ..models import BaseEnrollment, MaternalConsent


class BaseEnrollmentForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(BaseEnrollmentForm, self).clean()
        consent = MaternalConsent.objects.get(
            subject_identifier=cleaned_data.get('registered_subject').subject_identifier)
        if cleaned_data.get('report_datetime') < consent.consent_datetime:
            raise forms.ValidationError('Report datetime \'{}\' cannot be before the consent datetime of {}. '
                                        'Please correct'.format(cleaned_data.get('report_datetime'),
                                                                cleaned_data.get('consent_datetime')))
        if (
            cleaned_data.get('verbal_hiv_status') == 'NEVER' or
            cleaned_data.get('verbal_hiv_status') == 'UNK' or
            cleaned_data.get('verbal_hiv_status') == 'REFUSED'
        ):
            if cleaned_data.get('process_rapid_test') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'The current HIV status is {}. Rapid test cannot be NOT APPLICABLE.'
                    .format(cleaned_data.get('verbal_hiv_status')))
        if cleaned_data.get('verbal_hiv_status') == NEG:
            if cleaned_data.get('evidence_hiv_status') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Negative, Evidence of HIV '
                                            'result CANNOT be Not Applicable. Please correct.')
            if cleaned_data.get('valid_regimen') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Negative, "do records show that'
                                            ' participant takes ARVs" cannot be Not Applicable')
        if cleaned_data.get('verbal_hiv_status') == POS:
            if cleaned_data.get('evidence_hiv_status') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Positive, Evidence of HIV '
                                            'result CANNOT be Not Applicable. Please correct.')
            if cleaned_data.get('valid_regimen') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Positive, "do records show that'
                                            ' participant takes ARVs" cannot be Not Applicable')
        if cleaned_data.get('valid_regimen') == YES:
            if cleaned_data.get('valid_regimen_duration') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is on ARV. Regimen validity period'
                                            ' CANNOT be Not Applicable. Please correct.')
        else:
            if cleaned_data.get('valid_regimen_duration') != NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that there are no records of Participant taking ARVs. '
                                            'Regimen validity period should be Not Applicable. Please correct')
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
        return cleaned_data

    class Meta:
        model = BaseEnrollment
        fields = '__all__'
