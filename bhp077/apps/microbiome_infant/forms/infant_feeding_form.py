from ..models import InfantFeeding

from .base_infant_model_form import BaseInfantModelForm


class InfantFeedingForm(BaseInfantModelForm):

    class Meta:
        model = InfantFeeding
        fields = '__all__'
