from django.forms.models import ModelForm

from ..models import InfantFuDxItems


class InfantFuDxItems(ModelForm):

    class Meta:
        model = InfantFuDxItems
        fields = '__all__'
