from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from edc_constants.constants import NEW, YES, NO

from ..models import SrhServicesUtilization
from django.forms.util import ErrorList


class SrhServicesUtilizationForm(BaseMaternalModelForm):

    class Meta:
        model = SrhServicesUtilization
        fields = '__all__'

    def clean(self):
        cleaned_data = super(SrhServicesUtilizationForm, self).clean()
        if cleaned_data.get('seen_at_clinic') == NO:
            if not cleaned_data.get('reason_unseen_clinic'):
                raise forms.ValidationError(
                    'If have not you been seen in that clinic since your last visit with us. why not?')
        if 'is_contraceptive_initiated' in cleaned_data.keys():
            self.validate_m2m(
                label='chronic condition',
                leading=cleaned_data.get('is_contraceptive_initiated'),
                m2m=cleaned_data.get('contraceptive_methods')
            )
        if cleaned_data.get('is_contraceptive_initiated') == NO:
            if not cleaned_data.get('reason_not_initiated'):
                self._errors["reason_not_initiated"] = \
                    ErrorList([u"This field is required."])
                raise forms.ValidationError(
                    'If have not initiated contraceptive method, please provide reason.')
        else:
            if cleaned_data.get('reason_not_initiated'):
                self._errors["reason_not_initiated"] = \
                    ErrorList([u"Don't answer this question, since you have initiated contraceptive."])
                raise forms.ValidationError(
                    "Don't answer this question, since you have initiated contraceptive.")
        return cleaned_data
