from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import BaseMother
from edc_constants.constants import NO, YES


class BaseMotherForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(BaseMotherForm, self).clean()
        if cleaned_data.get('systolic_bp ') < cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError('Systolic blood pressure cannot be lower than the diastolic blood preassure.'
                                        ' Please correct.')
        return cleaned_data

    class Meta:
        model = BaseMother
        fields = '__all__'
