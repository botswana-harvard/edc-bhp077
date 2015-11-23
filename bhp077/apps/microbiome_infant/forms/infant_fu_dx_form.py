from ..models import InfantFuDx, InfantFuDxItems

from .base_infant_model_form import BaseInfantModelForm


class InfantFuDxForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuDx
        fields = '__all__'


class InfantFuDxItemsForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuDxItems
        fields = '__all__'
