from django.forms.models import ModelForm

from ..models import InfantFu


class InfantFuForm(ModelForm):

    class Meta:
        model = InfantFu
        fields = '__all__'
