from ..models import InfantFuNewMedItems

from .base_infant_model_form import BaseInfantModelForm


class InfantFuNewMedItemsForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuNewMedItems
        fields = '__all__'
