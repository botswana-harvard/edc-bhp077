from django.forms.models import ModelForm

from ..models import InfantFuNewMedItems


class InfantFuNewMedItemsForm(ModelForm):

    class Meta:
        model = InfantFuNewMedItems
        fields = '__all__'
