from base_maternal_model_form import BaseMaternalModelForm
from ..models import MaternalArvPreg, MaternalArv


class MaternalArvPregForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalArv
        fields = '__all__'
