from django import forms

from ..models import InfantBirthFeedVaccine, InfantVaccines

from .base_infant_model_form import BaseInfantModelForm

from bhp077.apps.microbiome_maternal.models import MaternalConsent
from ..models import InfantBirth


class InfantBirthFeedVaccineForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthFeedVaccineForm, self).clean()
        self.validate_report_datetime(cleaned_data, 'report_datetime')
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

    class Meta:
        model = InfantBirthFeedVaccine
        fields = '__all__'


class InfantVaccinesForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantVaccinesForm, self).clean()
        self.validate_vaccine_date(cleaned_data)
        return cleaned_data

    def validate_vaccine_date(self, cleaned_data):
        try:
            subject_identifier = cleaned_data.get('infant_birth_feed_vaccine').infant_visit.appointment.registered_subject.subject_identifier
            infant_birth = InfantBirth.objects.get(registered_subject__subject_identifier=subject_identifier)
            if cleaned_data.get('vaccine_date') < infant_birth.dob:
                raise forms.ValidationError('Vaccine date CANNOT be before DOB.')
        except InfantBirth.DoesNotExist:
            raise forms.ValidationError('Infant Birth does not exist.')

    class Meta:
        model = InfantVaccines
        fields = '__all__'
