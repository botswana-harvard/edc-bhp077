from django.forms.models import ModelForm

from ..models import InfantFuPhysical


class InfantFuPhysicalForm(ModelForm):

    class Meta:
        model = InfantFuPhysical
        fields = '__all__'
