from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from microbiome.apps.mb.choices import OFF_STUDY_REASON

from ..models import MaternalOffStudy, MaternalConsent

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalOffStudyForm (BaseMaternalModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(MaternalOffStudyForm, self).clean()
        self.validate_offstudy_date()
        return cleaned_data

    def validate_offstudy_date(self):
        cleaned_data = self.cleaned_data
        try:
            subject_identifier = cleaned_data.get(
                'maternal_visit').appointment.registered_subject.subject_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=subject_identifier)
            try:
                if cleaned_data.get('offstudy_date') < maternal_consent.consent_datetime.date():
                    raise forms.ValidationError("Off study date cannot be before consent date")
                if cleaned_data.get('offstudy_date') < maternal_consent.dob:
                    raise forms.ValidationError("Off study date cannot be before dob")
            except AttributeError:
                pass
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = MaternalOffStudy
