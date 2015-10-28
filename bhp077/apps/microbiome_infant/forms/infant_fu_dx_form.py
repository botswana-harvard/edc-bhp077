from ..models import InfantFuDx

from .base_infant_model_form import BaseInfantModelForm


class InfantFuDxForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuDx
        fields = '__all__'
