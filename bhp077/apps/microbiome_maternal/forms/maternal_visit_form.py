from edc_consent.forms import BaseConsentedModelForm

from ..models import MaternalVisit


class MaternalVisitForm (BaseConsentedModelForm):

    class Meta:
        model = MaternalVisit
        fields = '__all__'
