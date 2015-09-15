from django.forms import ModelForm

from ..models import InfantArvProph


class InfantArvProphForm(ModelForm):

    class Meta:
        model = InfantArvProph
        fields = '__all__'
