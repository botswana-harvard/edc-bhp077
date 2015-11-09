from ..models import InfantBirthData

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthDataForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthData
        fields = '__all__'
