from django import forms

from edc_constants.constants import YES

from ..models import MaternalDeath, MaternalConsent

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalDeathForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalDeathForm, self).clean()
        self.validate_report_datetime('death_date')
        self.validate_participant_hospitalized()
        self.validate_days_hospitalized()
        return cleaned_data

    def validate_participant_hospitalized(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('participant_hospitalized') == YES:
            if not cleaned_data.get('death_reason_hospitalized'):
                raise forms.ValidationError(
                    'If the participant was hospitalized, what was '
                    'the primary reason for hospitalisation?'
                )
        else:
            if cleaned_data.get('death_reason_hospitalized'):
                raise forms.ValidationError(
                    'If the participant was not hospitalized, please do '
                    'not provide primary reason for hospitalisation.'
                )

    def validate_days_hospitalized(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('participant_hospitalized') == YES:
            if cleaned_data.get('days_hospitalized') > 0:
                raise forms.ValidationError(
                    'If the participant was hospitalized, please provide number of '
                    'days the participant was hospitalised.')

    def validate_report_datetime(self, field):
        cleaned_data = self.cleaned_data
        try:
            relative_identifier = cleaned_data.get(
                'maternal_visit').appointment.registered_subject.subject_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=relative_identifier)
            if cleaned_data.get(field) < maternal_consent.consent_datetime.date():
                raise forms.ValidationError("{} CANNOT be before consent datetime".format(field.title()))
            if cleaned_data.get(field) < maternal_consent.dob:
                raise forms.ValidationError("{} CANNOT be before dob".format(field.title()))
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = MaternalDeath
        fields = '__all__'
