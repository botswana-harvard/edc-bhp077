from django.forms import ModelForm

from ..models import MaternalLocator


class MaternalLocatorForm(ModelForm):

    class Meta:
        model = MaternalLocator
        fields = '__all__'
