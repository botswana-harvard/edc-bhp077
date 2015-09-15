from django.forms.models import ModelForm

from ..models import InfantFuNewMed


class InfantFuNewMedForm(ModelForm):

    class Meta:
        model = InfantFuNewMed
        fields = '__all__'
