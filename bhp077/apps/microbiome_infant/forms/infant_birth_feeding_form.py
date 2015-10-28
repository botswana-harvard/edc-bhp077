from ..models import InfantBirthFeedVaccine

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthFeedVaccineForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthFeedVaccine
        fields = '__all__'
