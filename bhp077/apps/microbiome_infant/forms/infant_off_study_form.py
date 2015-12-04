from django import forms
from django.contrib.admin.widgets import (AdminRadioSelect,
                                          AdminRadioFieldRenderer)

from bhp077.apps.microbiome_maternal.models import MaternalConsent
from bhp077.apps.microbiome_infant.choices import OFF_STUDY_REASON

from ..forms import BaseInfantModelForm
from ..models import InfantOffStudy


class InfantOffStudyForm(BaseInfantModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = InfantOffStudy
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_offstudy_date(cleaned_data, 'offstudy_date')
        return super(InfantOffStudyForm, self).clean()

    def validate_offstudy_date(self, cleaned_data, field):
        try:
            subject_identifier = cleaned_data.get('infant_visit').\
                appointment.registered_subject.relative_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=subject_identifier)
            try:
                if (cleaned_data.get(field) <
                        maternal_consent.consent_datetime.date()):
                    raise forms.ValidationError("{} CANNOT be befor"
                                                "e consent datetime"
                                                "".format(field.title()))
                if cleaned_data.get(field) < maternal_consent.dob:
                    raise forms.ValidationError("{} "
                                                "CANNOT be before dob"
                                                "".format(field.title()))
            except AttributeError as err:
                print err
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')
