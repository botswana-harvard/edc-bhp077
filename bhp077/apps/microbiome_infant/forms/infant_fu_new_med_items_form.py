from django.forms.models import ModelForm

from ..models import InfantFuNewMedItems

from .base_infant_model_form import BaseInfantModelForm

class InfantFuNewMedItemsForm(ModelForm):

    class Meta:
        model = InfantFuNewMedItems
        fields = '__all__'
