from edc_consent.forms.base_consent_form import BaseConsentForm

from ..models import PostnatalEnrollment


class PostnatalEnrollmentForm(BaseConsentForm):

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
