from .base_infant_model_form import BaseInfantModelForm

from ..models import InfantFuDxItems


class InfantFuDxItems(BaseInfantModelForm):

    class Meta:
        model = InfantFuDxItems
        fields = '__all__'
