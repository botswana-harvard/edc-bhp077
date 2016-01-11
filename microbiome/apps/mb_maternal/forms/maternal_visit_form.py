from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.form.forms import BaseModelForm
from microbiome.apps.mb.choices import VISIT_REASON, VISIT_INFO_SOURCE, MATERNAL_VISIT_STUDY_STATUS, INFO_PROVIDER

from ..models import MaternalVisit, MaternalConsent
from edc_constants.constants import ON_STUDY, MISSED_VISIT
from edc_visit_tracking.forms import VisitFormMixin


class MaternalVisitForm (VisitFormMixin, BaseModelForm):

    participant_label = 'mother'

    study_status = forms.ChoiceField(
        label='What is the mother\'s current study status',
        choices=MATERNAL_VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(MaternalVisitForm, self).clean()
        MaternalVisit(**cleaned_data).has_previous_visit_or_raise(forms.ValidationError)
        try:
            subject_identifier = cleaned_data.get('appointment').registered_subject.subject_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=subject_identifier)
            if cleaned_data.get("report_datetime") < maternal_consent.consent_datetime:
                raise forms.ValidationError("Report datetime CANNOT be before consent datetime")
            if cleaned_data.get("report_datetime").date() < maternal_consent.dob:
                raise forms.ValidationError("Report datetime CANNOT be before DOB")
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = MaternalVisit(**self.cleaned_data)
        instance.subject_failed_eligibility(forms.ValidationError)

        return cleaned_data

    class Meta:
        model = MaternalVisit
        fields = '__all__'
