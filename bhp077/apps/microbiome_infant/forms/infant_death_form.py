#from .base_model_form import BaseModelForm
from django import forms

from edc_constants.constants import YES, NO

from bhp077.apps.microbiome_infant.forms import BaseInfantModelForm
from bhp077.apps.microbiome_maternal.models import MaternalConsent

from ..models import InfantDeath, InfantVisit


class InfantDeathForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantDeathForm, self).clean()
        self.validate_report_datetime(cleaned_data, 'death_date')
        self.validate_participant_hospitalized(cleaned_data)
        self.validate_days_hospitalized(cleaned_data)
        return cleaned_data

    def validate_participant_hospitalized(self, cleaned_data):
        if cleaned_data.get('participant_hospitalized') == YES:
            if not cleaned_data.get('death_reason_hospitalized'):
                raise forms.ValidationError(
                    'If the participant was hospitalized, what was the primary reason for hospitalisation?'
                )
        else:
            if cleaned_data.get('death_reason_hospitalized'):
                raise forms.ValidationError(
                    'If the participant was not hospitalized, please do not provide primary reason for hospitalisation.'
                )

    def validate_days_hospitalized(self, cleaned_data):
        if cleaned_data.get('participant_hospitalized') == YES:
            if cleaned_data.get('days_hospitalized') > 0:
                raise forms.ValidationError(
                        'If the participant was hospitalized, please provide number of days the participant was hospitalised.'
                    )

    def validate_report_datetime(self, cleaned_data, field):
        try:
            relative_identifier = cleaned_data.get('infant_visit').appointment.registered_subject.relative_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=relative_identifier)
            if cleaned_data.get(field) < maternal_consent.consent_datetime.date():
                raise forms.ValidationError("{} CANNOT be before consent datetime".format(field.title()))
            if cleaned_data.get(field) < maternal_consent.dob:
                raise forms.ValidationError("{} CANNOT be before dob".format(field.title()))
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = InfantDeath
        fields = '__all__'
