from django.forms import ModelForm

from ...models.infant import InfantBirth


class InfantBirthForm(ModelForm):

    class Meta:
        model = InfantBirth
        fields = '__all__'
