from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalPostFuMed, MaternalPostFuMedItems
from edc_constants.constants import NO, YES


class MaternalPostFuMedForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalPostFuMedForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalPostFuMed
        fields = '__all__'


class MaternalPostFuMedItemsForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalPostFuMedItemsForm, self).clean()
        if cleaned_data.get('date_stoped') < cleaned_data.get('date_first_medication'):
            raise forms.ValidationError('Date stopped medication is before date started medications. Please correct')
        return cleaned_data

    class Meta:
        model = MaternalPostFuMedItems
        fields = '__all__'
