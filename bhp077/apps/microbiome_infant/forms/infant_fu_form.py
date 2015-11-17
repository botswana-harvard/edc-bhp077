from ..models import InfantFu
from .base_infant_model_form import BaseInfantModelForm


class InfantFuForm(BaseInfantModelForm):

    class Meta:
        model = InfantFu
        fields = '__all__'
