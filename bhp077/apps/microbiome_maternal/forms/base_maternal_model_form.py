from edc_consent.forms import BaseConsentedModelForm

from ..models import MaternalVisit


class BaseMaternalModelForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseMaternalModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['maternal_visit'].queryset = MaternalVisit.objects.filter(
                pk=self.instance.maternal_visit.pk)
        except:
            pass
