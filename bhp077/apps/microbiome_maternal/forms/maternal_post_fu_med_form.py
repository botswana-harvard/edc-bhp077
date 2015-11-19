from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalPostFuMed, MaternalPostFuDx, MaternalPostFuDxT
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
        return cleaned_data

    class Meta:
        model = MaternalPostFuMed
        fields = '__all__'
