from django.forms.models import ModelForm

from ...models.infant import InfantDeath


class InfantDeathForm(ModelForm):

    class Meta:
        model = InfantDeath
        fields = '__all__'
