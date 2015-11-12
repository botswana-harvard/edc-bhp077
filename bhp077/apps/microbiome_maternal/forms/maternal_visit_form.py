from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc.base.form.forms import BaseModelForm

from ..models import MaternalVisit, MaternalConsent
from bhp077.apps.microbiome.choices import VISIT_REASON, VISIT_INFO_SOURCE


class MaternalVisitForm (BaseModelForm):

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):

        cleaned_data = self.cleaned_data
        maternal_consent = MaternalConsent.objects.filter(
            registered_subject__subject_identifier=cleaned_data.get('maternal_visit').appointment.registered_subject.subject_identifier)
        if not cleaned_data.get("report_datetime"):
            raise forms.ValidationError("Please fill in the date and time")
        if cleaned_data.get("report_datetime") < maternal_consent.consent_datetime:
            raise forms.ValidationError("Report datetime CANNOT be before consent_datetime")
        if cleaned_data.get("report_datetime") < maternal_consent.dob:
            raise forms.ValidationError("Report datetime CANNOT be before DOB")

        super(MaternalVisitForm, self).clean()

    class Meta:
        model = MaternalVisit
        fields = '__all__'
