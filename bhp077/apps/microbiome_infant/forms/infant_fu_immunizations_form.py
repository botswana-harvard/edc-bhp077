from ..models import InfantFuImmunizations

from .base_infant_model_form import BaseInfantModelForm


class InfantFuImmunizationsForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuImmunizations
        fields = '__all__'
