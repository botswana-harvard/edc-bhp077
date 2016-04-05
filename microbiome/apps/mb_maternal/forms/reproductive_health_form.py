from base_maternal_model_form import BaseMaternalModelForm

from ..models import ReproductiveHealth


class ReproductiveHealthForm(BaseMaternalModelForm):

    class Meta:
        model = ReproductiveHealth
        fields = '__all__'
