from base_maternal_model_form import BaseMaternalModelForm

from ..models import SexualReproductiveHealth


class SexualReproductiveHealthForm(BaseMaternalModelForm):

    class Meta:
        model = SexualReproductiveHealth
        fields = '__all__'
