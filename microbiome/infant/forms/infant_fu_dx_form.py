from django.forms.models import ModelForm

from ..models import InfantFuDx


class InfantFuDxForm(ModelForm):

    class Meta:
        model = InfantFuDx
        fields = '__all__'
