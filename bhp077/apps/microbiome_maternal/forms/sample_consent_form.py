from django import forms
from django.forms import ModelForm

from edc_constants.constants import YES, NO

from ..models import SampleConsent, MaternalConsent


class SampleConsentForm(ModelForm):

    def clean(self):
        cleaned_data = super(SampleConsentForm, self).clean()
        primary_consent = MaternalConsent.objects.filter(
            registered_subject__subject_identifier=cleaned_data.get('registered_subject').subject_identifier)
        if primary_consent:
            if cleaned_data.get("may_store_samples") == YES:
                if cleaned_data.get('is_literate') != primary_consent[0].is_literate:
                    raise forms.ValidationError("Sample Consent and Maternal Consent literacy "
                                                "answers do not match. Please Correct!")
                if cleaned_data.get('witness_name') != primary_consent[0].witness_name:
                    raise forms.ValidationError("Sample Consent and Maternal Consent witness names"
                                                "do not match. Please Correct!")
                if cleaned_data.get("consent_benefits") != YES:
                    raise forms.ValidationError("If may_store_samples is YES, ensure that sample"
                                                " storage benefits is explained to and understood by"
                                                " participant.")
        if cleaned_data.get('is_literate', None) == NO and not cleaned_data.get('witness_name', None):
            raise forms.ValidationError('You wrote subject is illiterate. Please provide the name of a witness here and with signature on the paper document.')
        if cleaned_data.get('is_literate') == YES and cleaned_data.get('witness_name', None):
            raise forms.ValidationError('You wrote subject is literate. The name of a witness is NOT required.')
        return cleaned_data

    class Meta:
        model = SampleConsent
        fields = '__all__'
