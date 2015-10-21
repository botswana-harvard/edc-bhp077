from ..models import InfantArvProph

from .base_infant_model_form import BaseInfantModelForm


class InfantArvProphForm(BaseInfantModelForm):

    class Meta:
        model = InfantArvProph
        fields = '__all__'
