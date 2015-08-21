from django.forms.models import ModelForm

from microbiome.models.microbiome_infant import InfantDeath


class InfantDeathForm(ModelForm):

    class Meta:
        model = InfantDeath
        fields = '__all__'
