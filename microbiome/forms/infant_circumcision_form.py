from django.forms import ModelForm

from ..models import InfantCircumcision


class InfantCircumcisionForm(ModelForm):

    class Meta:
        model = InfantCircumcision
        fields = '__all__'
