from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalInfected


class MaternalInfectedForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalInfected
        fields = '__all__'
