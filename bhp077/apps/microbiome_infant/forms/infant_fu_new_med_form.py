from ..models import InfantFuNewMed

from .base_infant_model_form import BaseInfantModelForm


class InfantFuNewMedForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuNewMed
        fields = '__all__'
