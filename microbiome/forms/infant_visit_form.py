from django.forms.models import ModelForm

from ..models import InfantVisit


class InfantVisit(ModelForm):

    class Meta:
        model = InfantVisit
        fields = '__all__'
