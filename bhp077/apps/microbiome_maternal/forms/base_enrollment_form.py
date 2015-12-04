from django import forms

from edc_constants.constants import POS, NEG, NOT_APPLICABLE, YES, NO

from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import BaseEnrollment, MaternalConsent, SpecimenConsent


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
            if cleaned_data.get('rapid_test_done') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'The current HIV status is {}. Rapid test cannot be NOT APPLICABLE.'
                    .format(cleaned_data.get('verbal_hiv_status')))
            if cleaned_data.get('rapid_test_done') == NO:
                raise forms.ValidationError("Participant verbal HIV status is {}. You must "
                                            "conduct HIV rapid testing today to continue with "
                                            "the eligibility screen".format(cleaned_data.get('verbal_hiv_status')))
        if cleaned_data.get("week32_test") == YES:
            if not cleaned_data.get("week32_result"):
                raise forms.ValidationError('Please provide test result at week 32.')
        else:
            if cleaned_data.get("week32_result"):
                raise forms.ValidationError(
                    'You mentioned testing was not done at 32weeks yet provided a test result.')
        if cleaned_data.get('verbal_hiv_status') == NEG:
            if cleaned_data.get('evidence_hiv_status') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Negative, Evidence of HIV '
                                            'result CANNOT be Not Applicable. Please correct.')
            if not cleaned_data.get('valid_regimen') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Negative.'
                                            ' Answer for REGIMEN should be Not Applicable.')
            if not cleaned_data.get('valid_regimen_duration') == NOT_APPLICABLE:
                raise forms.ValidationError('You have indicated that the participant is Negative.'
                                            ' Answer for REGIMEN DURATION should be Not Applicable.')
            if cleaned_data.get('evidence_hiv_status') == NO:
                if not cleaned_data.get('rapid_test_done') == YES:
                    raise forms.ValidationError("Participant is NEG and has no doc evidence. "
                                                "Rapid test is REQUIRED. Please Correct")
        if cleaned_data.get('verbal_hiv_status') == POS:
            if cleaned_data.get('evidence_hiv_status') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is Positive, Evidence of HIV '
                    'result CANNOT be Not Applicable. Please correct.')
            if cleaned_data.get('valid_regimen') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is Positive, "do records show that'
                    ' participant takes ARVs" cannot be Not Applicable.')
            if cleaned_data.get('evidence_hiv_status') == YES:
                if cleaned_data.get('rapid_test_done') == YES:
                    raise forms.ValidationError('DO NOT PROCESS RAPID TEST. PARTICIPANT IS POS and HAS EVIDENCE.')
        if cleaned_data.get('valid_regimen') == YES:
            if cleaned_data.get('valid_regimen_duration') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is on ARV. Regimen validity period'
                    ' CANNOT be Not Applicable. Please correct.')
        else:
            if cleaned_data.get('valid_regimen_duration') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that there are no records of Participant taking ARVs. '
                    'Regimen validity period should be Not Applicable. Please correct.')
        # week32 result and verbal status comparison
        if (cleaned_data.get("week32_result") == POS and cleaned_data.get("verbal_hiv_status") != POS or
                cleaned_data.get("week32_result") == NEG and cleaned_data.get("verbal_hiv_status") != NEG):
            raise forms.ValidationError('The verbal_hiv_status and result at 32weeks should be the same!')

        if cleaned_data.get('rapid_test_done') == YES:
            # date of rapid test is required if rapid test processed is indicated as Yes
            if not cleaned_data.get('rapid_test_date'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was processed. Please provide the date.')
            # if rapid test was done, result should be indicated
            if not cleaned_data.get('rapid_test_result'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was processed. Please provide a result.')
        else:
            if cleaned_data.get('rapid_test_date'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was NOT processed, yet rapid test date was'
                    ' provided. Please correct.')
            if cleaned_data.get('rapid_test_result'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was NOT processed, yet rapid test result '
                    'was provided. Please correct.')
        if not SpecimenConsent.objects.filter(
                registered_subject__subject_identifier=cleaned_data.get(
                    'registered_subject').subject_identifier).exists():
            raise forms.ValidationError("Please ensure to save the SAMPLE CONSENT before "
                                        "completing Enrollment")
        return cleaned_data

    class Meta:
        model = BaseEnrollment
        fields = '__all__'
