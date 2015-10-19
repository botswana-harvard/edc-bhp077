from django.forms.models import ModelForm

from ..models import InfantVisit


class InfantVisitForm(ModelForm):

    class Meta:
        model = InfantVisit
        fields = '__all__'
