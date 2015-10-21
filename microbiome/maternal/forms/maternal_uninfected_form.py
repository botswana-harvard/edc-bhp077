from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalUninfected


class MaternalUninfectedForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalUninfected
        fields = '__all__'
