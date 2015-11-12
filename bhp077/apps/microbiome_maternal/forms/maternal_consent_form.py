from django import forms

# from edc_consent.forms import BaseSubjectConsentForm
from edc_consent.forms.base_consent_form import BaseConsentForm

from ..models import MaternalConsent


class MaternalConsentForm(BaseConsentForm):

    def clean(self):
        self.cleaned_data['gender'] = 'F'
        cleaned_data = super(MaternalConsentForm, self).clean()
        if cleaned_data.get('identity_type') == 'OMANG' and cleaned_data.get('identity')[4] != '2':
            raise forms.ValidationError('Identity provided indicates participant is Male. Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalConsent
        fields = '__all__'
