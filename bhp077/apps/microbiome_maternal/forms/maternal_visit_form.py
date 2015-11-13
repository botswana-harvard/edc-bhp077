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
        cleaned_data = super(MaternalVisitForm, self).clean()
        try:
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=cleaned_data.get('appointment').registered_subject.subject_identifier)
            if cleaned_data.get("report_datetime") < maternal_consent.consent_datetime:
                raise forms.ValidationError("Report datetime CANNOT be before consent datetime")
            if cleaned_data.get("report_datetime").date() < maternal_consent.dob:
                raise forms.ValidationError("Report datetime CANNOT be before DOB")
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')
        if cleaned_data.get('reason') == 'unscheduled' and not cleaned_data.get('reason_unscheduled'):
                raise forms.ValidationError('You indicated that this is an unscheduled visit. Please '
                                            'provide a reason for the unscheduled visit.')
        if cleaned_data.get('reason') != 'unscheduled' and cleaned_data.get('reason_unscheduled'):
                raise forms.ValidationError('You indicated that this is NOT an unscheduled visit, yet provided a '
                                            'reason why it is unscheduled. Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalVisit
        fields = '__all__'
