from django import forms

from ..models import InfantBirthExam, InfantBirth
from bhp077.apps.microbiome_maternal.models import MaternalConsent

from .base_infant_model_form import BaseInfantModelForm

from edc_constants.constants import YES, NO


class InfantBirthExamForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthExam
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantBirthExamForm, self).clean()
        self.validate_report_datetime(cleaned_data, 'report_datetime')
        #self.validate_report_datetime(cleaned_data, 'infant_exam_date')
        self.validate_gender(cleaned_data)
        self.validate_general_activity(cleaned_data)
        self.validate_heent_exam(cleaned_data)
        self.validate_resp_exam(cleaned_data)
        self.validate_cardiac_exam(cleaned_data)
        return cleaned_data

    def validate_report_datetime(self, cleaned_data, field):
        try:
            relative_identifier = cleaned_data.get('infant_visit').appointment.registered_subject.relative_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=relative_identifier)
            if cleaned_data.get(field) < maternal_consent.consent_datetime:
                raise forms.ValidationError("{} CANNOT be before consent datetime".format(field.title()))
            if cleaned_data.get(field).date() < maternal_consent.dob:
                raise forms.ValidationError("{} CANNOT be before dob".format(field.title()))
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    def validate_gender(self, cleaned_data):
        infant_birth = InfantBirth.objects.get(
            registered_subject=cleaned_data.get('infant_visit').appointment.registered_subject)
        if not infant_birth.gender == cleaned_data.get('gender'):
            raise forms.ValidationError(
                'Gender mismatch you specified {} for infant birth and infant birth exam {}'.format(
                    infant_birth.gender, cleaned_data.get('gender')
                ))

    def validate_general_activity(self, cleaned_data):
        if cleaned_data.get('general_activity') == 'ABNORMAL':
            if not cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError('If abnormal, please specify.')

    def validate_heent_exam(self, cleaned_data):
        if not cleaned_data.get('heent_exam') == NO:
            if cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'If HEENT Exam is normal or not evaluated, Do not answer the following Question (Q10).'
                )
        elif cleaned_data.get('heent_exam') == NO:
            if not cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'Provide answer to Q10.'
                )

    def validate_resp_exam(self, cleaned_data):
        if not cleaned_data.get('resp_exam') == NO:
            if cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'If Respiratory Exam is normal, Do not answer the following Question (Q12).'
                )
        elif cleaned_data.get('resp_exam') == NO:
            if not cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'Provide answer to Q12.'
                )

    def validate_cardiac_exam(self, cleaned_data):
        if not cleaned_data.get('cardiac_exam') == NO:
            if cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'If Cardiac Exam is normal, Do not answer the following Question (Q14).'
                )
        elif cleaned_data.get('cardiac_exam') == NO:
            if not cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'Provide answer to Q14.'
                )
