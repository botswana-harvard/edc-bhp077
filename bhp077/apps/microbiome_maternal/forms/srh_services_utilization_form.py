from base_maternal_model_form import BaseMaternalModelForm

from ..models import SrhServicesUtilization


class SrhServicesUtilizationForm(BaseMaternalModelForm):

    class Meta:
        model = SrhServicesUtilization
        fields = '__all__'
