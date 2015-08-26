from django.forms.models import ModelForm

from ..models import MaternalEnrollArv


class MaternalEnrollArvForm(ModelForm):

    class Meta:
        model = MaternalEnrollArv
        fields = '__all__'
