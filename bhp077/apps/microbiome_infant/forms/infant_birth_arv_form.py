from ..models import InfantBirthArv

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthArvForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthArv
        fields = '__all__'
