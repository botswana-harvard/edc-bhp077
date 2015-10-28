from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalDemographics


class MaternalDemographicsForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalDemographics
        fields = '__all__'
