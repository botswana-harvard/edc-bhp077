from django import forms
from django.forms.util import ErrorList

from edc_constants.constants import NO

from ..models import MaternalSrh

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalSrhForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalSrh
        fields = '__all__'

    def clean(self):
        cleaned_data = super(MaternalSrhForm, self).clean()
        if cleaned_data.get('seen_at_clinic') == NO:
            if not cleaned_data.get('reason_unseen_clinic'):
                raise forms.ValidationError(
                    'If you have not been seen in that clinic since your last visit with us, why not?')
        if 'is_contraceptive_initiated' in cleaned_data.keys():
            self.validate_m2m(
                label='contraceptive method',
                leading=cleaned_data.get('is_contraceptive_initiated'),
                m2m=cleaned_data.get('contra')
            )
        if cleaned_data.get('is_contraceptive_initiated') == NO:
            if not cleaned_data.get('reason_not_initiated'):
                self._errors["reason_not_initiated"] = ErrorList(["This field is required."])
                raise forms.ValidationError(
                    'If have not initiated contraceptive method, please provide reason.')
        else:
            if cleaned_data.get('reason_not_initiated'):
                self._errors["reason_not_initiated"] = ErrorList(
                    ["Don't answer this question, since you have initiated contraceptive."])
                raise forms.ValidationError(
                    "Don't answer this question, since you have initiated contraceptive.")
        return cleaned_data
