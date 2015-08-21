from django.forms.models import ModelForm

from microbiome.models.microbiome_infant import InfantBirthFeedVaccine


class InfantBirthFeedVaccineForm(ModelForm):

    class Meta:
        model = InfantBirthFeedVaccine
        fields = '__all__'
