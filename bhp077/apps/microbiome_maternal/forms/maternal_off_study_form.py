from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

# from edc.subject.off_study.forms import BaseOffStudyForm
from bhp077.apps.microbiome.choices import OFF_STUDY_REASON
from bhp077.apps.microbiome_maternal.models import MaternalConsent

from .base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalOffStudy


class MaternalOffStudyForm (BaseMaternalModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(MaternalOffStudyForm, self).clean()
        self.validate_offstudy_date(cleaned_data, 'offstudy_date')
        return cleaned_data

    def validate_offstudy_date(self, cleaned_data, field):
        try:
            subject_identifier = cleaned_data.get('maternal_visit').appointment.registered_subject.subject_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=subject_identifier)
            try:
                if cleaned_data.get(field) < maternal_consent.consent_datetime.date():
                    raise forms.ValidationError("{} CANNOT be before consent datetime".format(field.title()))
                if cleaned_data.get(field) < maternal_consent.dob:
                    raise forms.ValidationError("{} CANNOT be before dob".format(field.title()))
            except AttributeError as err:
                print err
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = MaternalOffStudy
