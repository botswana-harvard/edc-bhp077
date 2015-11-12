from django import forms
from django.forms import ModelForm

from edc_constants.constants import YES, NO

from ..models import SampleConsent, MaternalConsent


class SampleConsentForm(ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        primary_consent = MaternalConsent.objects.filter(
            registered_subject__subject_identifier=cleaned_data.get('registered_subject').subject_identifier)
        if primary_consent:
            if cleaned_data.get("may_store_samples") == YES:
                if cleaned_data.get('is_literate') != primary_consent[0].is_literate:
                    raise forms.ValidationError("Sample Consent and Maternal Consent literacy "
                                                "answers do not match. Please Correct!")
        return super(SampleConsentForm, self).clean()

    class Meta:
        model = SampleConsent
        fields = '__all__'
