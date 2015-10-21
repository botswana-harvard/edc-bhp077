from ..models import InfantBirth

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirth
        fields = '__all__'
