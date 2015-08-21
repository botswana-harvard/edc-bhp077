from django.forms import ModelForm

from microbiome.models.microbiome_infant import InfantBirth


class InfantBirthForm(ModelForm):

    class Meta:
        model = InfantBirth
        fields = '__all__'
