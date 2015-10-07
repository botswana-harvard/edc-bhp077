from django.forms import ModelForm

from ..models import SampleConsent


class SampleConsentForm(ModelForm):

    def clean(self):
        clean_data = super(SampleConsentForm, self).clean()
        return clean_data

    class Meta:
        model = SampleConsent
        fields = '__all__'
