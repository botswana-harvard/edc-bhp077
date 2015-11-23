from ..models import InfantBirthFeedVaccine, InfantVaccines

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthFeedVaccineForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthFeedVaccine
        fields = '__all__'



class InfantVaccinesForm(BaseInfantModelForm):

    class Meta:
        model = InfantVaccines
        fields = '__all__'