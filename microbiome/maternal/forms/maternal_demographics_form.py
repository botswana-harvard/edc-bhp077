from django.forms import ModelForm

from ..models import MaternalDemographics


class MaternalDemographicsForm(ModelForm):

    class Meta:
        model = MaternalDemographics
        fields = '__all__'
