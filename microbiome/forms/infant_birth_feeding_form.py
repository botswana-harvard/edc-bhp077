from django.forms.models import ModelForm

from ..models import InfantBirthFeedVaccine


class InfantBirthFeedVaccineForm(ModelForm):

    class Meta:
        model = InfantBirthFeedVaccine
        fields = '__all__'
