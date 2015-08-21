from django.forms import ModelForm
from microbiome.models.microbiome_maternal import MaternalLocator


class MaternalLocatorForm(ModelForm):

    class Meta:
        model = MaternalLocator
        fields = '__all__'
