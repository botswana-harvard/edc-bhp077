from django.forms.models import ModelForm
from ..models import MaternalArvPreg, MaternalArv


class MaternalArvPregForm(ModelForm):

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvForm(ModelForm):

    class Meta:
        model = MaternalArv
        fields = '__all__'
