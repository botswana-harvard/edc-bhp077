from ..models import InfantFuImmunizations, VaccinesReceived, VaccinesMissed

from .base_infant_model_form import BaseInfantModelForm


class InfantFuImmunizationsForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuImmunizations
        fields = '__all__'


class VaccinesReceivedForm(BaseInfantModelForm):

    class Meta:
        model = VaccinesReceived
        fields = '__all__'


class VaccinesMissedForm(BaseInfantModelForm):

    class Meta:
        model = VaccinesMissed
        fields = '__all__'
