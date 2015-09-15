from django.forms.models import ModelForm

from ..models import InfantFuImmunizations


class InfantFuImmunizationsForm(ModelForm):

    class Meta:
        model = InfantFuImmunizations
        fields = '__all__'
