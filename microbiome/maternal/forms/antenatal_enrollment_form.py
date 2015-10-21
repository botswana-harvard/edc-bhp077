from edc_consent.forms.base_consent_form import BaseConsentForm

from ..models import AntenatalEnrollment


class AntenatalEnrollmentForm(BaseConsentForm):

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
