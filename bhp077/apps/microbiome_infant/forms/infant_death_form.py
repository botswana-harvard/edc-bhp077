from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import InfantDeath


class InfantDeathForm(BaseModelForm):

    class Meta:
        model = InfantDeath
        fields = '__all__'
