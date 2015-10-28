from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalDeath


class MaternalDeathForm (BaseMaternalModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('maternal_visit') or not cleaned_data.get('registered_subject'):
            raise forms.ValidationError('This field is required. Please fill it in')
        return super(MaternalDeathForm, self).clean()

    class Meta:
        model = MaternalDeath
