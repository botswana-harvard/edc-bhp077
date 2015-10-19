from django.forms import ModelForm

from ..models import MaternalConsent


class MaternalConsentForm(ModelForm):

    def clean(self):
        clean_data = super(MaternalConsentForm, self).clean()
        return clean_data

    class Meta:
        model = MaternalConsent
        fields = '__all__'
