from django import forms
from django.utils import timezone

from edc_constants.choices import NO
from bhp077.apps.microbiome.utils import weeks_between

from ..models import MaternalArvHistory, MaternalConsent

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalArvHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvHistoryForm, self).clean()
        self.validate_arv_interrupt(cleaned_data)
        self.validate_haart_start_date(cleaned_data)
        return cleaned_data

    def validate_arv_interrupt(self, cleaned_data):
        if cleaned_data.get('preg_on_haart') == NO:
            if cleaned_data.get('prior_preg') != 'interruption never restarted':
                raise forms.ValidationError(
                    'You indicated that the mother was NOT still on tripple ARV when she got pregnant. Yet stated {}. '
                    'Please correct.'.format(cleaned_data.get('prior_preg')))
        else:
            if cleaned_data.get('prior_preg') == 'interruption never restarted':
                raise forms.ValidationError('You indicated that the mother was still on tripple ARV when '
                                            'she got pregnant, yet you indicated that ARVs were interrupted '
                                            'and never restarted.')

    def validate_haart_start_date(self, cleaned_data):
        haart_start_date = cleaned_data.get('haart_start_date')
        if weeks_between(haart_start_date, timezone.now()) < 6:
            raise forms.ValidationError(
                "ARV start date (question 3) must be six weeks prior to today's date or greater.")
        try:
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=cleaned_data.get(
                    'maternal_visit').appointment.registered_subject.subject_identifier)
            if cleaned_data.get("report_datetime") < maternal_consent.consent_datetime:
                raise forms.ValidationError("Report datetime CANNOT be before consent datetime")
            if cleaned_data.get("haart_start_date") < maternal_consent.dob:
                raise forms.ValidationError("Date of triple antiretrovirals first started CANNOT be before DOB.")
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = MaternalArvHistory
        fields = '__all__'
