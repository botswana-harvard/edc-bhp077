from django import forms

from ..models import InfantStoolCollection
from .base_infant_model_form import BaseInfantModelForm


class InfantStoolCollectionForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stool_colection_time', None) > 24:
            raise forms.ValidationError("Stool collection time cannot exceed 24hours")

    class Meta:
        model = InfantStoolCollection
        fields = '__all__'
