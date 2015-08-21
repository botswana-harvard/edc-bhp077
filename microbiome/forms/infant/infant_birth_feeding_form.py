from django.forms.models import ModelForm

from ...models.infant import InfantBirthFeedVaccine


class InfantBirthFeedVaccineForm(ModelForm):

    class Meta:
        model = InfantBirthFeedVaccine
        fields = '__all__'
