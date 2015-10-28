from edc_consent.forms.base_consent_form import BaseConsentForm

from ..models import MaternalConsent


class MaternalConsentForm(BaseConsentForm):

    def clean(self):
        clean_data = super(MaternalConsentForm, self).clean()
        return clean_data

    class Meta:
        model = MaternalConsent
        fields = '__all__'
