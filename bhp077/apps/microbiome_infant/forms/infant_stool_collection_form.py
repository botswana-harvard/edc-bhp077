from django import forms
from django.forms.models import ModelForm

from ..models import InfantStoolCollection


class InfantStoolCollection(ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        # if stool collection was completed more than 24hours ago.
        if cleaned_data.get('stool_colection_time', None) > 24:
            raise forms.ValidationError("Stool collection time cannot exceed 24hours")

    class Meta:
        model = InfantStoolCollection
        fields = '__all__'