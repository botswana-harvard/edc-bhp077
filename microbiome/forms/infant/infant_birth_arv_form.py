from django.forms import ModelForm

from microbiome.models.microbiome_infant import InfantBirthArv


class InfantBirthArvForm(ModelForm):

    class Meta:
        model = InfantBirthArv
        fields = '__all__'
