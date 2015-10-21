from django.forms.models import ModelForm

from ..models import InfantFuNewMed

from .base_infant_model_form import BaseInfantModelForm


class InfantFuNewMedForm(ModelForm):

    class Meta:
        model = InfantFuNewMed
        fields = '__all__'
