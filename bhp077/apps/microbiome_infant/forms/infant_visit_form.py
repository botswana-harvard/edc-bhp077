from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from bhp077.apps.microbiome.choices import VISIT_REASON, VISIT_INFO_SOURCE
from bhp077.apps.microbiome_maternal.models import MaternalConsent

from ..models import InfantVisit
from .base_infant_model_form import BaseInfantModelForm


class InfantVisitForm(BaseInfantModelForm):

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        required=False,
        label='Source of information',
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(InfantVisitForm, self).clean()
        self.validate_reason_death(cleaned_data)
        self.validate_reason_lost_and_completed(cleaned_data)
        self.validate_reason_missed(cleaned_data)
        self.validate_survival_status(cleaned_data)

        if not cleaned_data.get('reason') == 'missed':
            if not cleaned_data.get('info_source'):
                raise forms.ValidationError("Provide source of information.")

        try:
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=cleaned_data.get('appointment').registered_subject.relative_identifier)
            if cleaned_data.get("report_datetime") < maternal_consent.consent_datetime:
                raise forms.ValidationError("Report datetime CANNOT be before consent datetime")
            if cleaned_data.get("report_datetime").date() < maternal_consent.dob:
                raise forms.ValidationError("Report datetime CANNOT be before DOB")
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')
        return cleaned_data

    def validate_reason_death(self, cleaned_data):
        if cleaned_data.get('reason') == 'death':
            if not cleaned_data.get('survival_status') == 'DEAD':
                raise forms.ValidationError("You should select Deceased for survival status.")
            if not cleaned_data.get('study_status') == 'offstudy':
                raise forms.ValidationError("You should select offstudy for the participant's current study status.")

    def validate_reason_lost_and_completed(self, cleaned_data):
        if cleaned_data.get('reason') in ['lost', 'off study']:
            if not cleaned_data.get('study_status') == 'offstudy':
                raise forms.ValidationError("You should select offstudy for the participant's current study status.")

    def validate_reason_missed(self, cleaned_data):
        if cleaned_data.get('reason') == 'missed':
            if not cleaned_data.get('reason_missed'):
                raise forms.ValidationError("Provide reason scheduled visit was missed.")
            # if cleaned_data.get('info_source'):
            #     raise forms.ValidationError("Do not provide source of information.")

    def validate_survival_status(self, cleaned_data):
        if cleaned_data.get('survival_status') in ['ALIVE', 'DEAD']:
            if not cleaned_data.get('date_last_alive'):
                raise forms.ValidationError("Provide Date last known alive.")

    class Meta:
        model = InfantVisit
        fields = '__all__'
