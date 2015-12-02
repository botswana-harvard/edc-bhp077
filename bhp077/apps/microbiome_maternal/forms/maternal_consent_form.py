from django import forms
from django.utils import timezone

from edc_consent.forms.base_consent_form import BaseConsentForm

from ..models import MaternalConsent, MaternalEligibility 
from edc.subject.registration.models import registered_subject
from dateutil.relativedelta import relativedelta


class MaternalConsentForm(BaseConsentForm):

    def clean(self):
        self.cleaned_data['gender'] = 'F'
        cleaned_data = super(MaternalConsentForm, self).clean()
        if cleaned_data.get('identity_type') == 'OMANG' and cleaned_data.get('identity')[4] != '2':
            raise forms.ValidationError('Identity provided indicates participant is Male. Please correct.')
        self.validate_eligibility_age(cleaned_data)
        return cleaned_data

    def validate_eligibility_age(self, cleaned_data):
        consent_age = relativedelta(timezone.now().date(), cleaned_data.get('dob')).years
        eligibility_age = MaternalEligibility.objects.get(registered_subject=cleaned_data.get('registered_subject')).age_in_years
        if consent_age != eligibility_age:
            raise forms.ValidationError('In Maternal Eligibility you indicated the participant is {}, '
                                        'but age derived from the DOB is {}.'.format(eligibility_age, consent_age))

    class Meta:
        model = MaternalConsent
        fields = '__all__'
