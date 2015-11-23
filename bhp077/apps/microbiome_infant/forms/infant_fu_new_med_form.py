from ..models import InfantFuNewMed, InfantFuNewMedItems

from .base_infant_model_form import BaseInfantModelForm


class InfantFuNewMedForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuNewMed
        fields = '__all__'


class InfantFuNewMedItemsForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuNewMedItems
        fields = '__all__'
