from ..models import InfantFuPhysical

from .base_infant_model_form import BaseInfantModelForm


class InfantFuPhysicalForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuPhysical
        fields = '__all__'
