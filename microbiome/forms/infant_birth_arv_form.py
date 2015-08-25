from django.forms import ModelForm

from ..models import InfantBirthArv


class InfantBirthArvForm(ModelForm):

    class Meta:
        model = InfantBirthArv
        fields = '__all__'
