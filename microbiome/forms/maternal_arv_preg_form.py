from django.forms.models import ModelForm
from ..models import (
    MaternalArvPreg, MaternalArvPregHistory, MaternalArvPPHistory, MaternalArv)


class MaternalArvPregForm(ModelForm):

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvPregHistoryForm(ModelForm):

    class Meta:
        model = MaternalArvPregHistory
        fields = '__all__'


class MaternalArvPPHistoryForm(ModelForm):

    class Meta:
        model = MaternalArvPPHistory
        fields = '__all__'


class MaternalArvForm(ModelForm):

    class Meta:
        model = MaternalArv
        fields = '__all__'
