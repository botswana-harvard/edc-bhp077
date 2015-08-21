from django.forms import ModelForm
from ...models.maternal import MaternalLocator


class MaternalLocatorForm(ModelForm):

    class Meta:
        model = MaternalLocator
        fields = '__all__'
