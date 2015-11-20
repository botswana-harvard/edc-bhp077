from django import forms

from ..models import MaternalInfected

from .base_mother_form import BaseMotherForm


class MaternalInfectedForm(BaseMotherForm):

    def clean(self):
        cleaned_data = super(MaternalInfectedForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalInfected
        fields = '__all__'
