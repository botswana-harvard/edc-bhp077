from edc.base.form.forms import BaseModelForm

from ..models import MaternalConsent


class MaternalConsentForm(BaseModelForm):

    def clean(self):
        clean_data = super(MaternalConsentForm, self).clean()
        return clean_data

    class Meta:
        model = MaternalConsent
        fields = '__all__'
