from edc_consent.forms import BaseSpecimenConsentForm

from ..models import SpecimenConsent, MaternalConsent


class SpecimenConsentForm(BaseSpecimenConsentForm):

    STUDY_CONSENT = MaternalConsent

    class Meta:
        model = SpecimenConsent
        fields = '__all__'
