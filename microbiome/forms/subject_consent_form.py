from django.forms import ModelForm

from ..models import SubjectConsent


class SubjectConsentForm(ModelForm):


    def clean(self):
        clean_data = super(SubjectConsentForm, self).clean()
        return clean_data

    class Meta:
        model = SubjectConsent
        fields = '__all__'
